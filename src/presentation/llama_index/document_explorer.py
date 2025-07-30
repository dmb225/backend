import asyncio
import os
import tempfile
from typing import Any

import llama_index.core
import streamlit as st
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import ChatMemoryBuffer, SimpleComposableMemory, VectorMemory
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.groq import Groq

# Enable simple tracing for observability
llama_index.core.set_global_handler("simple")

# Initialize LLM and embedding model
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise OSError("Missing GROQ_API_KEY environment variable.")

llm = Groq(model="llama3-70b-8192", api_key=groq_api_key)
embedding_model = OllamaEmbedding(model_name="nomic-embed-text")


# Memory setup
chat_memory = ChatMemoryBuffer.from_defaults()
vector_memory = VectorMemory.from_defaults(
    embed_model=embedding_model, retriever_kwargs={"similarity_top_k": 3}
)
composable_memory = SimpleComposableMemory.from_defaults(
    primary_memory=chat_memory, secondary_memory_sources=[vector_memory]
)


async def process_query(query: str, index: Any) -> None:
    # Store user message
    user_msg = ChatMessage(role="user", content=query)
    composable_memory.put(user_msg)

    # Recall memory
    memory_items = composable_memory.get(query)
    recalled_memory = "\n".join(f"{msg.role.capitalize()}: {msg.content}" for msg in memory_items)

    # Retrieve document chunks
    retriever = index.as_retriever(similarity_top_k=3)
    retrieved_nodes = retriever.retrieve(query)
    document_context = "\n".join(node.get_content() for node in retrieved_nodes)

    # Construct full prompt
    prompt = f"""You are answering questions based on uploaded documents and memory.

Memory:
{recalled_memory}

Document Chunks:
{document_context}

User Question:
{query}
"""

    # Generate response
    response = llm.complete(prompt)

    # Store assistant reply
    assistant_msg = ChatMessage(role="assistant", content=response.text)
    composable_memory.put(assistant_msg)

    # Display result
    st.subheader("Answer")
    st.write(response.text)


def main() -> None:
    # Streamlit setup
    st.set_page_config(page_title="Multi-Turn Document Q&A")
    st.title("Multi-Turn Document Q&A with Your PDFs")
    st.markdown("Upload one or more PDF documents, then ask questions or request a summary.")

    # Inputs
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    query = st.text_input("Enter your question:")
    summarize_clicked = st.button("Summarize Document")

    # Index documents only once per session
    if uploaded_files and "documents" not in st.session_state:
        with (
            st.spinner("Loading and indexing documents..."),
            tempfile.TemporaryDirectory() as temp_dir,
        ):
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            docs = SimpleDirectoryReader(input_dir=temp_dir).load_data()
            idx = VectorStoreIndex.from_documents(docs, embed_model=embedding_model)

            st.session_state.documents = docs
            st.session_state.index = idx

    # Retrieve document index and parsed docs
    documents = st.session_state.get("documents")
    index = st.session_state.get("index")

    if query and index:
        asyncio.run(process_query(query, index))

    # Summarization
    if summarize_clicked and documents:
        with st.spinner("Generating summary..."):
            full_text = "\n".join(doc.text for doc in documents)
            prompt = f"Please summarize the following document:\n\n{full_text}"
            response = llm.complete(prompt)
            st.subheader("Document Summary")
            st.write(response.text)


if __name__ == "__main__":
    main()
