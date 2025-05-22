import asyncio
import logging
import os

from dotenv import load_dotenv
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging


async def get_response(llm: Groq) -> None:
    user_prompt = "What is the capital of France?"
    response = await llm.acomplete(user_prompt)
    logging.info(f"User prompt: {user_prompt}")
    logging.info(f"LLM response: {response.text}")


def main() -> None:
    load_dotenv()
    setup_logging()

    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise OSError("Missing GROQ_API_KEY environment variable.")

    llm = Groq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        api_key=groq_api_key,
        temperature=0.3,
        max_tokens=512,
        system_prompt="You are an AI assistant that provides concise answers based on user's query",
    )

    asyncio.run(get_response(llm))


if __name__ == "__main__":
    main()
