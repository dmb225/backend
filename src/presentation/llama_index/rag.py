import logging
import os
import subprocess
import tempfile

import streamlit as st
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.groq import Groq

from src.logging_config import setup_logging


def ensure_ollama_model(model_name: str) -> None:
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
        logging.info(f"Successfully pulled model: {model_name}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to pull model '{model_name}'. Error: {e}") from e


def execute_rag(llm: Groq, model_name: str) -> None:
    # Ensure embedding model is pulled
    ensure_ollama_model(model_name)

    st.title("Q&A with Your Documents")
    st.markdown("Upload your `.pdf` files to build a semantic search index and ask questions.")
    uploaded_files = st.file_uploader("Upload text files", type="pdf", accept_multiple_files=True)
    query = st.text_input("Ask a question about the documents")
    if uploaded_files and query:
        with (
            st.spinner("Processing documents and building index..."),
            tempfile.TemporaryDirectory() as temp_dir,
        ):
            # Save uploaded files to a temporary directory
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            # Load documents
            documents = SimpleDirectoryReader(input_dir=temp_dir).load_data()

            # Create vector index
            embedding_model = OllamaEmbedding(model_name=model_name)
            index = VectorStoreIndex.from_documents(documents, embed_model=embedding_model)
            index.storage_context.persist()

            # Retrieve and query
            query_engine = index.as_query_engine(llm=llm)
            response = query_engine.query(query)

            # Display results
            st.subheader("Answer:")
            st.write(str(response))


def main() -> None:
    setup_logging()
    load_dotenv()

    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise OSError("Missing GROQ_API_KEY environment variable.")

    rag_llm = Groq(model="llama3-70b-8192", api_key=groq_api_key)
    execute_rag(rag_llm, "nomic-embed-text")


if __name__ == "__main__":
    main()
