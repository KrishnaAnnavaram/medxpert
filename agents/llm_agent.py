import os
import openai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Chat history
chat_history = []

def chat_with_user(user_input):
    chat_history.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )

    answer = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": answer})
    return answer

import openai

def summarize_medicines(columns, rows):
    """
    Builds an HTML summary for each medicine with:
    - Tablet name (bold)
    - Image (if available)
    - GPT-4 based friendly explanation
    """

    if not rows:
        return "Sorry, I couldn't find any medicines matching your symptoms."

    html_blocks = []

    for row in rows:
        row_data = dict(zip(columns, row))

        name = row_data.get("Medicine_Name", "Unknown")
        image_url = row_data.get("Image_URL", "")
        dosage = row_data.get("Composition", "Not available")
        uses = row_data.get("Uses", "Not available")
        side_effects = row_data.get("Side_effects", "Not listed")
        manufacturer = row_data.get("Manufacturer", "Unknown")
        rating = row_data.get("Excellent_Review_Percent", "N/A")

        # Prompt to GPT
        prompt = f"""
You are a helpful medical assistant with years of experience. Based on the details provided below, generate a friendly and informative explanation of the medicine in paragraph form.

Details:
- Name: {name}
- Dosage: {dosage}
- Uses: {uses}
- Side Effects: {side_effects}
- Manufacturer: {manufacturer}
- Excellent Review Percent: {rating}%
make all section names in bold 

Explain this medicine to a non-technical person. Cover:
- What the medicine is and why it's used
- When and how to take it
- Where to store it
- Common side effects
- Any precautions or advice
Dont tell to completly ask user to consult with doctor instead use your knoweldge and say what are best dosage and when to take it (like after meal or before meal) and how to take.
🎯 Keep the tone warm, professional, and easy to understand. Don't use bullet points. Just return a natural paragraph like you're speaking to the patient directly.
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You summarize medicine data for patients."},
                    {"role": "user", "content": prompt}
                ]
            )
            gpt_summary = response.choices[0].message.content.strip()

        except Exception as e:
            gpt_summary = f"⚠️ GPT error: {e}"

        # HTML block
        html_block = f"""
<div style="margin-bottom: 40px; padding: 15px; border-radius: 10px; background-color: #f8f9fa;">
    <h3 style="color:#222;"><strong>💊 {name}</strong></h3>
    <img src="{image_url}" alt="{name}" style="width: 300px; margin-top: 10px; border-radius: 10px;" />
    <p style="margin-top: 15px; font-size: 16px;">{gpt_summary.replace('\n', '<br>')}</p>
</div>
        """

        html_blocks.append(html_block)

    return "\n".join(html_blocks)
