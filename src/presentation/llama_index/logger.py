import os

import llama_index.core
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.groq import Groq

load_dotenv()

# Enable basic debugging
llama_index.core.set_global_handler("simple")

llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROG_API_KEY"))
embedding_model = OllamaEmbedding(model_name="nomic-embed-text")

# Creating sample documents
documents = [
    Document(text="The Eiffel Tower is located in Paris, France."),
    Document(text="The Great Wall of China is a historic fortification in China."),
]

# Indexing documents and enabling query execution
index = VectorStoreIndex.from_documents(documents, embed_model=embedding_model)
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Where is the Eiffel Tower located?")
