import logging
import os

from dotenv import load_dotenv
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging

setup_logging()
load_dotenv()


llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY"))


def simple_llm_chat() -> None:
    logging.info("💬 Welcome to Simple LLM Chat (no memory).")
    logging.info("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            logging.info("👋 Goodbye!")
            break

        response = llm.complete(user_input)
        logging.info(f"LLM: {response.text}\n")


simple_llm_chat()
