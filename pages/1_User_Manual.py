import streamlit as st
from modules.user_manual_generator import generate_user_manual

# ✅ Set page config FIRST
st.set_page_config(
    page_title="User Manual Generator",
    page_icon="📘",
    layout="centered"
)

# ✅ Title (only once)
st.title("📘 Medicine User Manual Generator")

st.markdown("This tool helps you generate a detailed, patient-friendly manual for any medicine in the language of your choice.")

# --- 1. Medicine Name Input ---
medicine_name = st.text_input("🔍 Enter the medicine name")

# --- 2. Language Selection ---
language = st.text_input("🌐 Enter the language for the manual (e.g., English, Hindi, Telugu, Spanish)")

# --- 3. Generate Button ---
if st.button("🧠 Medexpert Generate Manual"):
    if not medicine_name or not language:
        st.warning("⚠️ Please enter both the medicine name and language.")
    else:
        # 🧪 Simulated input (replace with actual DB call if needed)
        dummy_row = {
            "Medicine_Name": medicine_name,
            "Composition": "500mg Paracetamol",
            "Uses": "Fever, body pain, and inflammation",
            "Side_effects": "Nausea, dizziness, allergic reactions",
            "Manufacturer": "Generic Pharma Ltd.",
            "Excellent_Review_Percent": "89"
        }

        # 🧠 Generate the manual using GPT-4
        with st.spinner("Generating your manual..."):
            manual = generate_user_manual(dummy_row, language)

        # ✅ Display and download
        st.success("✅ Manual generated successfully!")
        st.markdown("### 📄 Medicine User Manual")
        st.markdown(manual)
        st.download_button("📥 Download Manual", manual, file_name=f"{medicine_name}_manual.txt")
