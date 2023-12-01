import asyncio
import inspect
import json
import os
import sys
from collections import defaultdict
from typing import Any, AsyncIterator, Callable, Optional, TypeVar

import docstring_parser
import httpx
import httpx_sse
import pydantic

T = TypeVar("T")

if sys.version_info < (3, 10):

    async def anext(ait: AsyncIterator[T]) -> T:
        return await ait.__anext__()


class Agent:
    def __init__(
        self,
        *,
        system_prompt: str = "You are a helpful assistant",
        api_key: Optional[str] = None,
        base_url: str = "https://api.openai.com/v1",
        timeout: float = 30.0,
    ) -> None:
        self.system_prompt = system_prompt

        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise RuntimeError(
                "You either need to pass the 'api_key' parameter or"
                "set the OPENAI_API_KEY environment variable."
            )
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            timeout=timeout,
        )

        self._functions: dict[str, Callable] = {}
        self.schemas: list[dict[str, Any]] = []

    def register(self, fn: Callable) -> Callable:
        model = pydantic.create_model(  # type: ignore[call-overload]
            fn.__name__,
            **{
                parameter.name: (
                    parameter.annotation,
                    parameter.default
                    if parameter.default is not inspect.Parameter.empty
                    else ...,
                )
                for parameter in inspect.signature(fn).parameters.values()
            },
        )
        schema = model.model_json_schema()

        # FIXME: instead of manually fixing the schema here, let's define an OpenAI one
        schema = {
            "name": schema.pop("title"),
            "parameters": schema,
        }

        docstring = docstring_parser.parse(fn.__doc__)
        schema["description"] = docstring.short_description

        parameter_descriptions = {
            param.arg_name: param.description for param in docstring.params
        }
        properties = schema["parameters"]["properties"]
        for parameter_name in list(properties.keys()):
            description = parameter_descriptions.get(parameter_name)
            if description:
                properties[parameter_name]["description"] = description

            del properties[parameter_name]["title"]

        self._functions[schema["name"]] = fn
        self.schemas.append(schema)

        return fn

    def answer(
        self,
        prompt: str,
        *,
        max_calls: int = 3,
        model: str = "gpt-3.5-turbo-0613",
        **kwargs: Any,
    ) -> str:
        async def wrapper() -> str:
            return "".join(
                [
                    chunk
                    async for chunk in self.aanswer_stream(
                        prompt, max_calls=max_calls, model=model, **kwargs
                    )
                ]
            )

        return asyncio.run(wrapper())

    async def aanswer_stream(
        self,
        prompt: str,
        *,
        max_calls: int = 3,
        model: str = "gpt-3.5-turbo-0613",
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        reserved_params = ["messages", "functions", "stream"]
        if any(param in kwargs for param in reserved_params):
            raise ValueError(
                f"The parameters {', '.join(repr(param) for param in reserved_params)} "
                f"are reserved by call_center and mut not be passed, but got {kwargs}."
            )

        messages: list[dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]
        for num_call in range(max_calls + 1):
            async with httpx_sse.aconnect_sse(
                self._client,
                "POST",
                "/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "messages": messages,
                    "functions": self.schemas,
                    "stream": True,
                    "model": model,
                    **kwargs,
                },
            ) as event_source:
                # FIXME: error handling
                events = event_source.aiter_sse()
                event = await anext(events)
                delta = json.loads(event.data)["choices"][0]["delta"]

                if delta["content"] is not None:
                    yield delta["content"]

                    async for event in events:
                        choice = json.loads(event.data)["choices"][0]
                        if choice["finish_reason"] is not None:
                            return

                        yield choice["delta"]["content"]
                elif num_call == max_calls:
                    raise RuntimeError(
                        f"Unable to obtain an answer with {max_calls} function calls."
                    )

                function_call_chunks = defaultdict(list)
                for key, value_chunk in delta["function_call"].items():
                    function_call_chunks[key].append(value_chunk)
                async for event in events:
                    choice = json.loads(event.data)["choices"][0]
                    if choice["finish_reason"] is not None:
                        break

                    for key, value_chunk in choice["delta"]["function_call"].items():
                        function_call_chunks[key].append(value_chunk)

            function_call = {
                key: "".join(value_chunks)
                for key, value_chunks in function_call_chunks.items()
            }
            name = function_call["name"]
            arguments = json.loads(function_call["arguments"])

            return_value = self._functions[name](**arguments)

            messages.extend(
                [
                    {
                        "role": "assistant",
                        "content": None,
                        "function_call": function_call,
                    },
                    {
                        "role": "function",
                        "name": name,
                        "content": json.dumps(return_value),
                    },
                ]
            )
