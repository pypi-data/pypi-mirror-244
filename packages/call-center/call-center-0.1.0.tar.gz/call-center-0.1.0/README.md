# `call-center`

```python
from call_center import Agent

user = "pmeier"
agent = Agent(system_prompt=f"The current user is {user}")


@agent.register
def get_products(user: str):
    """Get the available products for the user

    :param user: User to get products for.
    """
    return [f"Product{idx}" for idx in {"pmeier": [3, 5, 7, 14]}.get(user, [])]


print(agent.answer("What products are available for me?"))
print(get_products(user))
```

```
The available products for you are: Product3, Product5, Product7, and Product14.
['Product3', 'Product5', 'Product7', 'Product14']
```

```python
@agent.register
def rank_products(products: list[str]):
    """Rank products by revenue.

    :param products: List of products to rank.
    """
    return sorted(products)


async def answer(prompt):
    async for chunk in agent.aanswer_stream(prompt):
        print(chunk, end="")
    print()


import asyncio

asyncio.run(answer("What are the top three products?"))
print(rank_products(get_products(user))[:3])
```

```
The top three products are:
1. Product14
2. Product3
3. Product5
['Product14', 'Product3', 'Product5']
```
