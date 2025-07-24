import asyncio
import logging
import os

from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import ChatMemoryBuffer, SimpleComposableMemory, VectorMemory
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging

setup_logging()
load_dotenv()

# ----------------------------
# Step 1: Connect to LLM and embedding model
# ----------------------------
llm = Groq(
    model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY")
)  # Replace with your actual Groq API key
embedding_model = OllamaEmbedding(model_name="nomic-embed-text")

# ----------------------------
# Step 2: Set up memory components
# ----------------------------
vector_memory = VectorMemory.from_defaults(
    embed_model=embedding_model, retriever_kwargs={"similarity_top_k": 5}
)

chat_memory = ChatMemoryBuffer.from_defaults()

composable_memory = SimpleComposableMemory.from_defaults(
    primary_memory=chat_memory, secondary_memory_sources=[vector_memory]
)


# ----------------------------
# Step 3: Create a function to generate prompts with memory
# ----------------------------
def generate_prompt_with_memory(query: str) -> str:
    retrieved = composable_memory.get(query)
    if not retrieved:
        # No memory yet — skip context block
        return f"You are a helpful assistant.\n\nUser: {query}\nAssistant:"

    memory_context = "\n".join([f"{msg.role.capitalize()}: {msg.content}" for msg in retrieved])
    return f"""You are a helpful assistant.

        Here is what the user has shared in the past:
        {memory_context}

        User: {query}
        Assistant:"""


# ----------------------------
# Step 4: Interactive chat loop without agent or tool use
# ----------------------------
async def memory_aware_chat() -> None:
    logging.info(
        "Welcome to your memory-aware assistant (manual memory retrieval). Type 'exit' to quit.\n"
    )

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            logging.info("Goodbye!")
            break

        # Store the user input
        user_msg = ChatMessage(role="user", content=user_input)
        composable_memory.put(user_msg)

        # Retrieve memory and generate the prompt
        prompt = generate_prompt_with_memory(user_input)

        # Get response from the LLM
        response = await llm.acomplete(prompt)
        logging.info(f"Agent: {response.text}\n")

        # Store the assistant's response
        assistant_msg = ChatMessage(role="assistant", content=response.text)
        composable_memory.put(assistant_msg)


asyncio.run(memory_aware_chat())
