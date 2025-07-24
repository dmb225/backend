import asyncio
import logging
import os
import random
from typing import Any, cast

from dotenv import load_dotenv
from llama_index.core.agent.types import Task
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging

QUERIES = [
    "I want to know the status of my order with ID h45 and return my Galaxy Fit 2.",
    "Can you please give me a summary of the reviews for Galaxy Fit 2.",
    "Can you please find me a product within price 50.",
]


# Initialize the LLM instance for all agents
llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY"), verbose=True)


# --- Tool: Check order status ---
def fetch_order_status(order_id: str) -> str:
    logging.info(f"Fetching order status for order ID: {order_id}")
    statuses = ["Shipped", "In Transit", "Delivered", "Out for Delivery", "Cancelled"]
    status = random.choice(statuses)
    return f"Order {order_id} is currently: {status}"


# --- Tool: Process return request ---
def process_return(item_id: str) -> str:
    logging.info("Processing return request.")
    return f"Return request for item {item_id} has been initiated successfully."


# --- Tool: Search products ---
def search_products(price: int) -> list[dict[str, Any]]:
    logging.info("Searching for products.")
    logging.info(f"Price: {price}")
    sample_products = [
        {"name": "Galaxy Fit 2", "price": 99},
        {"name": "Samsung watch", "price": 199},
        {"name": "Fitbit Inspire", "price": 89},
        {"name": "Mi Band 6", "price": 45},
    ]

    filtered_product_list = [p for p in sample_products if cast(int, p["price"]) <= price]
    logging.info(f"Filtered_product_list: {filtered_product_list}")
    return filtered_product_list


# --- Tool: Summarize reviews ---
def summarize_reviews(product_name: str) -> str:
    logging.info(f"Summarizing reviews for product: {product_name}")
    reviews = {
        "Galaxy Fit 2": [
            "Great battery life!",
            "Very lightweight and comfortable.",
            "Lacks some features of premium models.",
        ],
        "Samsung Galaxy Watch 4": [
            "Excellent display and fast performance.",
            "Battery drains quickly.",
            "Great fitness tracking features.",
        ],
    }
    product_reviews = reviews.get(product_name, ["No reviews found."])
    summary = f"Summary for {product_name}: " + " ".join(product_reviews)
    return "Summary of the Product Reviews" + summary


# --- Planner tool logic ---
def planner_logic(query: str) -> list[Task]:
    logging.info("Planner logic called")
    tasks = []

    if "return" in query.lower():
        tasks.append(
            Task(
                tool_name="process_return",
                tool_args={"item_id": "Galaxy Fit 2"},
                input=query,
                memory={},
            )
        )

    if "status" in query.lower():
        tasks.append(
            Task(
                tool_name="fetch_order_status",
                tool_args={"order_id": "h45"},
                input=query,
                memory={},
            )
        )

    if "find" in query.lower() or "search" in query.lower():
        tasks.append(
            Task(tool_name="search_products", tool_args={"price": 50}, input=query, memory={})
        )

    if "summarize" in query.lower() or "summary" in query.lower():
        tasks.append(
            Task(
                tool_name="summarize_reviews",
                tool_args={"product_name": "Galaxy Fit 2"},
                input=query,
            )
        )

    return tasks


# Convert tools to FunctionTool
fetch_order_status_tool = FunctionTool.from_defaults(fn=fetch_order_status)
process_return_tool = FunctionTool.from_defaults(fn=process_return)
search_products_tool = FunctionTool.from_defaults(fn=search_products)
summarize_reviews_tool = FunctionTool.from_defaults(fn=summarize_reviews)
planner_tool = FunctionTool.from_defaults(fn=planner_logic)

# Define individual agents
order_agent = FunctionAgent(
    llm=llm,
    tools=[fetch_order_status_tool, process_return_tool],
    name="OrderSupportAgent",
    description="Handles order status checks and return requests.",
    system_prompt="You are an expert in order support. "
    "Answer only order-related queries such as order status and return.",
)

product_agent = FunctionAgent(
    llm=llm,
    tools=[search_products_tool],
    name="ProductExpertAgent",
    description="Finds products based on category and budget.",
    system_prompt="You are a product recommendation expert. Answer only product search queries.",
)

summarizer_agent = FunctionAgent(
    llm=llm,
    tools=[summarize_reviews_tool],
    name="SummarizerAgent",
    description="Summarizes user reviews for a given product.",
    system_prompt="You are an expert in summarizing product reviews. "
    "Summarize clearly and concisely.",
)

planner_agent = FunctionAgent(
    llm=llm,
    tools=[planner_tool],
    name="PlannerAgent",
    description="Analyzes the user query and "
    "splits it into subtasks that can be assigned to the available specialized agents.",
    system_prompt="You are a planning agent that analyzes complex user queries and "
    "divides them into actionable tasks to be handled by relaevant agents.",
)

# Create the agent workflow with Planner as the root
agent_workflow = AgentWorkflow(
    agents=[planner_agent, order_agent, product_agent, summarizer_agent],
    root_agent=planner_agent.name,
)


async def run_agent() -> None:
    for query in QUERIES:
        response = await agent_workflow.run(user_msg=query)
        logging.info(f"\nResponse: {response}\n")


def main() -> None:
    setup_logging()
    load_dotenv()

    asyncio.run(run_agent())


if __name__ == "__main__":
    main()
