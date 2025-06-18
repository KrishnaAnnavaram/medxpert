# qdrant_search_app.py

import streamlit as st
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# ✅ Setup
st.set_page_config(page_title="🔍 MedXpert - Qdrant Search", layout="centered")
st.title("💊 MedXpert - Semantic Medicine Search")

# Connect to local Qdrant
client = QdrantClient(host="localhost", port=6333)
collection_name = "medxpert_medicines"

# Load SentenceTransformer model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# User Input
query = st.text_input("Enter your symptom or keyword:", placeholder="e.g. fever, cold, infection")

if query:
    try:
        query_vector = embedding_model.encode(query).tolist()

        results = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=3,
            with_payload=True
        )

        if results:
            st.success("✅ Found Results")
            for i, result in enumerate(results, 1):
                payload = result.payload
                st.markdown(f"### 🧠 Match {i}: `{payload.get('medicine_name', 'Unknown')}`")
                st.markdown(f"📝 **Info**: {payload.get('text', '')}")
                st.markdown(f"🖼️ **Image Name**: `{payload.get('image_name', '')}`")
                st.markdown("---")
        else:
            st.warning("⚠️ No relevant results found in Qdrant.")

    except Exception as e:
        st.error(f"🚨 Error during search: {e}")
