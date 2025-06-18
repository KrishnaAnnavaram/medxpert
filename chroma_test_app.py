# chroma_test_app.py

import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

# Load environment variables (if any)
load_dotenv()

# ✅ NEW Chroma Client (Post-0.4.22 style)
chroma_client = chromadb.PersistentClient(path="medxpert/chroma_db_fresh")

# Load the ChromaDB collection
try:
    collection = chroma_client.get_collection(name="drug_images")
except Exception as e:
    st.error(f"❌ Failed to load vector DB collection: {e}")
    st.stop()

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# UI setup
st.set_page_config(page_title="🔬 ChromaDB Test", layout="centered")
st.title("🔍 MedXpert - Vector Search Test")
st.markdown("Search your ChromaDB drug image embeddings using a simple symptom or keyword.")

# User Input
query = st.text_input("💬 Enter a symptom or keyword:", placeholder="e.g. fever, infection, headache")

# Search on input
if query:
    try:
        query_embedding = embedding_model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        if results and results['documents']:
            st.success("✅ Top 3 Results Found!")
            for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
                st.markdown(f"### Result {i}")
                st.markdown(f"📃 **Extracted Text:** {doc[:200]}...")
                st.markdown(f"📦 **ZIP File:** `{meta.get('zip_file')}`")
                st.markdown(f"🖼️ **Image File:** `{meta.get('image_name')}`")
                st.markdown("---")
        else:
            st.warning("⚠️ No matching documents found.")

    except Exception as e:
        st.error(f"🚨 Error during vector search: {e}")
