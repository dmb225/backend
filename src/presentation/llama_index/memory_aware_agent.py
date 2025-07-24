import asyncio
import logging
import os

from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import ChatMemoryBuffer, SimpleComposableMemory, VectorMemory
from llama_index.core.tools import FunctionTool
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging

setup_logging()
load_dotenv()

# ----------------------------
# Step 1: Connect to LLM and embedding Model
# ----------------------------
llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY"))
embedding_model = OllamaEmbedding(model_name="nomic-embed-text")

# ----------------------------
# Step 2: Set up memory components
# ----------------------------
vector_memory = VectorMemory.from_defaults(
    embed_model=embedding_model,
    retriever_kwargs={"similarity_top_k": 5},  # allow broader recall
)

chat_memory = ChatMemoryBuffer.from_defaults()

composable_memory = SimpleComposableMemory.from_defaults(
    primary_memory=chat_memory, secondary_memory_sources=[vector_memory]
)


# ----------------------------
# Step 3: Define tool to recall memory
# ----------------------------
def recall_facts(query: str) -> str:
    msgs = composable_memory.get(query)
    if not msgs:
        return "Sorry, I couldn’t find anything in memory related to that."
    return "\n".join([f"{msg.role.capitalize()}: {msg.content}" for msg in msgs])


recall_tool = FunctionTool.from_defaults(fn=recall_facts)

# ----------------------------
# Step 4: Create the memory-aware agent
# ----------------------------
agent = FunctionAgent(
    name="MemoryAssistant",
    description="An assistant that remembers what you've shared and recalls it when needed.",
    system_prompt="You're a memory-aware assistant. Use memory to personalize responses. "
    "If needed, use the recall tool.",
    llm=llm,
    tools=[recall_tool],
    verbose=True,
)


# ----------------------------
# Step 5: Run the interactive chat loop
# ----------------------------
async def interactive_chat() -> None:
    logging.info("Welcome to your memory-aware AI assistant. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            logging.info("Goodbye!")
            break

        # Store user's message in memory
        user_msg = ChatMessage(role="user", content=user_input)
        composable_memory.put(user_msg)

        # Get agent response
        try:
            response = await agent.run(user_input)
        except Exception:
            logging.info("[Agent failed to call function, falling back to direct LLM response...]")
            fallback_response = await llm.acomplete(user_input)
            response = fallback_response.text

        # Store assistant's response in memory
        assistant_msg = ChatMessage(role="assistant", content=str(response))
        composable_memory.put(assistant_msg)

        logging.info(f"Agent: {response}\n")


# Start the chat
asyncio.run(interactive_chat())
