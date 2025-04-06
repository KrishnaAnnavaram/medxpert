import os
import openai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_user_manual(medicine_details: dict, language: str = "English") -> str:
    """
    Generates a multilingual user manual using GPT-4.

    Parameters:
    - medicine_details (dict): A dictionary containing fields such as:
        Medicine_Name, Composition, Uses, Side_effects, Manufacturer, Excellent_Review_Percent
    - language (str): Target language for the user manual (default is English)

    Returns:
    - str: The translated user manual content
    """

    prompt = f"""
You are a multilingual medical assistant. Write a detailed user manual for the following medicine.

Medicine Details:
- Name: {medicine_details.get("Medicine_Name", "N/A")}
- Dosage/Composition: {medicine_details.get("Composition", "N/A")}
- Uses: {medicine_details.get("Uses", "N/A")}
- Side Effects: {medicine_details.get("Side_effects", "N/A")}
- Manufacturer: {medicine_details.get("Manufacturer", "N/A")}
- Excellent Review Percent: {medicine_details.get("Excellent_Review_Percent", "N/A")}%

Instructions:
1. Write the manual in **{language}**.
2. Format the response in paragraph style.
3. Cover the following sections:
   - Introduction
   - Dosage Instructions
   - How and When to Take
   - Where to Store
   - Side Effects
   - Precautions
   - Manufacturer Information
   - Emergency Advice
4. Use a friendly and patient-safe tone, and ensure it’s easily understandable.

Output only the user manual content. Do not include any metadata, disclaimers, or labels.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a multilingual medical assistant that writes clear and helpful medicine instructions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ An error occurred while generating the manual: {e}"
