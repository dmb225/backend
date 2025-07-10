import asyncio
import logging
import os
import random

from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging

QUERIES = [
    "Where’s my order? Order ID: 12345",
    "Can I return this item? Item ID: ABC987",
    "Search for a laptop under 1000 dollars.",
]


# Tool to fetch order status
def get_order_status(order_id: str) -> str:
    status = random.choice(["Shipped", "In Transit", "Delivered", "Processing"])
    return f"Order {order_id} is currently {status}."


# Tool to check return policy
def process_return(item_id: str) -> str:
    return f"Return request for item {item_id} has been initiated."


# Tool to search products
def search_products(category: str, max_price: float) -> str:
    sample_products = {
        "laptop": ["Laptop A - $900", "Laptop B - $850", "Laptop C - $999"],
        "phone": ["Phone X - $700", "Phone Y - $650", "Phone Z - $800"],
    }
    products = sample_products.get(category.lower(), [])
    filtered_products = [p for p in products if float(p.split("$")[-1]) <= max_price]
    return (
        f"Found products: {', '.join(filtered_products)}"
        if filtered_products
        else "No products found."
    )


# Define tools
order_status_tool = FunctionTool.from_defaults(fn=get_order_status)
return_tool = FunctionTool.from_defaults(fn=process_return)
search_tool = FunctionTool.from_defaults(fn=search_products)


async def run_agent() -> None:
    # Initialize the LLM
    llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY"))

    # Create an agent with multiple tools
    agent = FunctionAgent(
        name="CustomerSupportAgent",
        description="An AI assistant for handling customer support queries.",
        system_prompt="You are a helpful assistant that can check order status, "
        "process returns, and search for products. When searching, "
        "extract the product category and price from the query and call the appropriate tool.",
        llm=llm,
        tools=[order_status_tool, return_tool, search_tool],
    )
    for query in QUERIES:
        response = await agent.run(user_msg=query)
        logging.info(f"User: {query}\nAgent: {response}\n")


def main() -> None:
    setup_logging()
    load_dotenv()

    asyncio.run(run_agent())


if __name__ == "__main__":
    main()
