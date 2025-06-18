# ocr_test_from_zip_cleaned.py

import zipfile
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter
import pytesseract
import re
import io

# === Configuration ===
zip_path = Path("data/dm_spl_monthly_update_mar2025/otc/20250302_1d4fcb76-22d1-7292-e063-6394a90af920.zip")
output_image_path = Path("debug_extracted_image.jpg")

# === Load and extract image from ZIP ===
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    image_names = [name for name in zip_ref.namelist() if name.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not image_names:
        print("❌ No image found inside the ZIP.")
        exit()

    first_image_name = image_names[0]
    print(f"✅ Extracting and reading image: {first_image_name}")

    with zip_ref.open(first_image_name) as image_file:
        img = Image.open(io.BytesIO(image_file.read()))

# === Preprocess image ===
img = ImageOps.grayscale(img)               # Convert to grayscale
img = img.filter(ImageFilter.SHARPEN)       # Sharpen the image
img = ImageOps.autocontrast(img)            # Enhance contrast
img.save(output_image_path)                 # Save for inspection

print(f"🖼 Image saved: {output_image_path} — open this to inspect OCR quality")

# === Run OCR with English language ===
text = pytesseract.image_to_string(img, lang="eng")

# === Clean text ===
def clean_ocr_text(t):
    t = t.strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^A-Za-z0-9.,:;()%-]+", " ", t)
    return t[:800]  # Limit to 800 characters

cleaned_text = clean_ocr_text(text)

# === Output result ===
print("\n🧠 OCR Extracted & Cleaned Text:")
print("-" * 60)
print(cleaned_text)
