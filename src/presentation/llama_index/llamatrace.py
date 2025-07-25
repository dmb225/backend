import logging
import os

import llama_index.core
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging

setup_logging()
load_dotenv()


PHOENIX_API_KEY = os.getenv("PHOENIX_API_KEY")
if not PHOENIX_API_KEY:
    raise ValueError("PHOENIX_API_KEY not found in environment variables.")
llama_index.core.set_global_handler(
    "arize_phoenix", endpoint="https://llamatrace.com/v1/traces", api_key=PHOENIX_API_KEY
)

llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY"))

embedding_model = OllamaEmbedding(model_name="nomic-embed-text")

documents = [
    Document(text="The Eiffel Tower is located in Paris, France."),
    Document(text="The Great Wall of China is a historic fortification in China."),
]
index = VectorStoreIndex.from_documents(documents, embed_model=embedding_model)
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Where is the Eiffel Tower located?")

logging.info("Traces have been sent to the LlamaTrace dashboard. See the dashboard!")
