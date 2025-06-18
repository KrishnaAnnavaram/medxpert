import os
import zipfile
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path
import pytesseract
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer

# Tesseract OCR path (Windows default)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Directories
DATA_DIR = Path("data")
OUTPUT_TEXT_DIR = Path("output/records")
OUTPUT_IMAGE_DIR = Path("output/images")

# Ensure output folders exist
OUTPUT_TEXT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# Init Qdrant
client = QdrantClient(host="localhost", port=6333)
collection_name = "medxpert_medicines"
if collection_name not in [col.name for col in client.get_collections().collections]:
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Parse XML file to extract required fields
def parse_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns = {'ns': 'urn:hl7-org:v3'}

    def get_text(tag):
        el = root.find(f".//ns:{tag}", ns)
        return el.text.strip() if el is not None and el.text else "Not available"

    return {
        "medicine_name": get_text("title"),
        "composition": get_text("activeIngredient"),
        "uses": get_text("indicationsAndUsage"),
        "how_to_use": get_text("dosageAndAdministration"),
        "where_to_store": get_text("storageAndHandling"),
        "side_effects": get_text("adverseReactions"),
        "manufacturer": get_text("manufacturer"),
        "who_can_use": get_text("useInSpecificPopulations")
    }

# Process ZIP files recursively
def process_zip(zip_path, month, category):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        extract_dir = Path("temp_extracted") / uuid.uuid4().hex
        zip_ref.extractall(extract_dir)

        xmls = list(extract_dir.glob("*.xml"))
        images = list(extract_dir.glob("*.jpg")) + list(extract_dir.glob("*.png"))

        if not xmls:
            return

        for xml_file in xmls:
            fields = parse_xml(xml_file)
            ocr_text = ""

            for image_file in images:
                try:
                    ocr_result = pytesseract.image_to_string(Image.open(image_file))
                    ocr_text += f"\n--- OCR from {image_file.name} ---\n{ocr_result}\n"

                    # Save image
                    img_out_dir = OUTPUT_IMAGE_DIR / month / category
                    img_out_dir.mkdir(parents=True, exist_ok=True)
                    img_out_path = img_out_dir / image_file.name
                    Image.open(image_file).save(img_out_path)

                except Exception as e:
                    print(f"OCR failed on {image_file}: {e}")

            # Combine everything into a text summary
            summary = f"""
Name: {fields['medicine_name']}
Composition: {fields['composition']}
Uses: {fields['uses']}
How to use: {fields['how_to_use']}
Where to store: {fields['where_to_store']}
Who can use: {fields['who_can_use']}
Side Effects: {fields['side_effects']}
Manufacturer: {fields['manufacturer']}

{ocr_text}
            """

            # Save to output text file
            text_id = uuid.uuid4().hex
            out_file = OUTPUT_TEXT_DIR / f"{text_id}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(summary.strip())

            # Embed and upload to Qdrant
            embedding = model.encode(summary.strip()).tolist()
            client.upsert(
                collection_name=collection_name,
                points=[
                    PointStruct(
                        id=text_id,
                        vector=embedding,
                        payload={
                            **fields,
                            "category": category,
                            "source_month": month,
                            "image_name": images[0].name if images else "None"
                        }
                    )
                ]
            )

        # Clean temp
        if extract_dir.exists():
            for item in extract_dir.rglob("*"):
                item.unlink()
            extract_dir.rmdir()

# Main loop
def run():
    for month_dir in DATA_DIR.glob("dm_spl_monthly_update_*/"):
        month = month_dir.name.replace("dm_spl_monthly_update_", "")
        for category_dir in month_dir.iterdir():
            if not category_dir.is_dir():
                continue
            category = category_dir.name
            for zip_file in category_dir.glob("*.zip"):
                try:
                    process_zip(zip_file, month, category)
                    print(f"✅ Processed {zip_file.name} ({month}/{category})")
                except Exception as e:
                    print(f"❌ Failed {zip_file.name} - {e}")

if __name__ == "__main__":
    run()
