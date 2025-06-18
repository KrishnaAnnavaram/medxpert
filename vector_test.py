from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Step 1: Connect to Qdrant
client = QdrantClient("localhost", port=6333)

# Step 2: Load the same embedding model used during ingestion
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 3: Enter your test query
query = "dog"
query_vector = model.encode(query).tolist()

# Step 4: Search Qdrant
results = client.search(
    collection_name="medxpert_medicines",
    query_vector=query_vector,
    limit=3,
    with_payload=True
)

# Step 5: Print results
for i, hit in enumerate(results):
    print(f"🔎 Result {i+1}")
    print("📦 Full Payload:", hit.payload)
    print("🧠 Score:", hit.score)
    print("-" * 50)

