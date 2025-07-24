import asyncio
import logging
import os

from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging

setup_logging()
load_dotenv()

# Connect to the Groq LLM
llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY"))


def greeting() -> str:
    return "Hi, can you please introduce yourself?"


greeting_tool = FunctionTool.from_defaults(fn=greeting, description="Greets the user")

agent = FunctionAgent(
    tools=[greeting_tool],
    llm=llm,
    system_prompt="You are an agent that can chat with the user.",
)


async def simple_llm_chat() -> None:
    logging.info("💬 Welcome to Simple Agent (no memory).")
    logging.info("Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ")
        if user_message.strip().lower() == "exit":
            logging.info("👋 Goodbye!")
            break

        # Run the agent with a user query
        agent_response = await agent.run(user_message)
        logging.info(f"Agent: {agent_response}")


# Run simple chat
asyncio.run(simple_llm_chat())
