import logging
import os

from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging

setup_logging()
load_dotenv()


# Initialize debug handler and callback manager
debug_handler = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([debug_handler])

# Initialize models
llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY"))
embedding_model = OllamaEmbedding(model_name="nomic-embed-text")

# Sample documents
documents = [
    Document(text="The Eiffel Tower is located in Paris, France."),
    Document(text="The Great Wall of China is a historic fortification in China."),
]

# Create the index with tracing enabled
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=embedding_model,
    callback_manager=callback_manager,  # ✅ Tracing enabled here
)

# Create a query engine from the index and connect it to the LLM
query_engine = index.as_query_engine(llm=llm)

response = query_engine.query("Where is the Eiffel Tower located?")
logging.info(response)
