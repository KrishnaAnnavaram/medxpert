from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

# ✅ Connect to local Qdrant
client = QdrantClient(host="localhost", port=6333)

# ✅ Create collection if not already created
collection_name = "medxpert_medicines"

if collection_name not in [col.name for col in client.get_collections().collections]:
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    print(f"✅ Created collection: {collection_name}")
else:
    print(f"📌 Collection already exists: {collection_name}")

# ✅ Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Example documents — you can later replace with OCR-based text
documents = [
    {
        "name": "Paracetamol",
        "text": "Paracetamol is used to reduce fever and treat mild to moderate pain.",
        "image": "img001.jpg"
    },
    {
        "name": "Ibuprofen",
        "text": "Ibuprofen is an NSAID used to relieve pain and inflammation.",
        "image": "img002.jpg"
    },
    {
        "name": "Amoxicillin",
        "text": "Amoxicillin is an antibiotic used to treat various bacterial infections.",
        "image": "img003.jpg"
    }
]

# ✅ Embed and insert documents
points = []
for doc in documents:
    embedding = model.encode(doc["text"]).tolist()
    points.append(
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "medicine_name": doc["name"],
                "text": doc["text"],
                "image_name": doc["image"]
            }
        )
    )

# ✅ Upload to Qdrant
client.upsert(collection_name=collection_name, points=points)
print(f"✅ Inserted {len(points)} documents into Qdrant.")
