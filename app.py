import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb
import requests
import httpx
import asyncio

# Constants
Ollama_GENERATE_URL = "http://localhost:11434/api/generate"
Ollama_EMBED_URL = "http://localhost:11434/api/embed"
Ollama_MODEL = "qwen2.5:0.5b"

# Initialize libraries
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma")

# Async function to send embedding request
async def send_embedding_request(new_embed):
    payload = {
        "model": Ollama_MODEL,
        "input": new_embed,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(Ollama_GENERATE_URL, json=payload)
        return response

# Check if the collection exists, if not, create it
collection_name = "embeddings"
try:
    collection = client.get_collection(collection_name)
except Exception as e:
    st.error(f"Error accessing collection: {e}")
    collection = client.create_collection(collection_name)

# Streamlit interface
st.title("Ollama Document Interaction Web-App")
st.write("This web-app allows you to interact with Ollama and ChromaDB.")

# Add a new document
new_embed = st.text_area("Enter a new feature for embedding:")
if new_embed:
    try:
        # Add the new document to the collection
        add_response = collection.add(
            documents=[new_embed],
            metadatas=[{"source": "user_input"}],
            ids=["id1"]
        )
        # Check if the document was added successfully
        st.write(f"Add response: {add_response}")  # Debugging output to see the result

        # Run async function in the background (non-blocking)
        asyncio.create_task(send_embedding_request(new_embed))
        st.success("Embedding added to ChromaDB. Processing the embedding in the background.")
    except Exception as e:
        st.error(f"Error embedding to model: {e}")

# Ask a question to Ollama
question = st.text_input("Ask a question:")
if question:
    payload = {
        "model": Ollama_MODEL,
        "prompt": question,
        "stream": False,
    }

    try:
        response = requests.post(Ollama_GENERATE_URL, json=payload)
        response.raise_for_status()
        st.success(f"Ollama response: {response.json()['response']}")
    except httpx.RequestError as e:
        st.error(f"Error while fetching response from Ollama API: {e}")
    except KeyError:
        st.error("Unexpected response format from Ollama API.")
