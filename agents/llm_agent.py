import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_history = []

# 🔹 General chat
def chat_with_user(user_input):
    chat_history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )
    answer = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": answer})
    return answer

# 🔹 Medicine summarization
def summarize_medicines(columns, rows):
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

        prompt = f"""
You are a helpful medical assistant. Based on the medicine details, create a friendly, patient-level explanation.

Details:
- Name: {name}
- Dosage: {dosage}
- Uses: {uses}
- Side Effects: {side_effects}
- Manufacturer: {manufacturer}
- Excellent Review Percent: {rating}%

Make section titles bold. Use a warm and professional tone. Avoid bullet points.
Return a paragraph that reads like you're talking to a patient.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You summarize medicine data for patients."},
                    {"role": "user", "content": prompt}
                ]
            )
            gpt_summary = response.choices[0].message.content.strip()
        except Exception as e:
            gpt_summary = f"⚠️ GPT error: {e}"

        summary_html = gpt_summary.replace('\n', '<br>')
        html_block = f"""
<div style="margin-bottom: 40px; padding: 15px; border-radius: 10px; background-color: #f8f9fa;">
    <h3 style="color:#222;"><strong>💊 {name}</strong></h3>
    <img src="{image_url}" alt="{name}" style="width: 300px; margin-top: 10px; border-radius: 10px;" />
    <p style="margin-top: 15px; font-size: 16px;">{summary_html}</p>
</div>
"""
        html_blocks.append(html_block)

    return "\n".join(html_blocks)

# 🔹 Classify user input
def classify_input_type(user_input):
    prompt = f"""
Classify the following user input into one of two categories:
- 'general_chat' (greetings, small talk, or questions about the assistant)
- 'symptom_query' (describing symptoms or asking for medicine recommendations)

Input: \"{user_input}\"

Respond with exactly one word: 'general_chat' or 'symptom_query'.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip().lower()

# 🔹 General replies
def generate_general_reply(user_input):
    prompt = f"""
You are MedXpert, a friendly and knowledgeable AI medical assistant.
Reply politely and informally to this general message: \"{user_input}\".

Keep the tone warm and professional. Reply in 1–2 lines.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# 🔹 Rephrase symptoms into medical keywords
def rephrase_symptom_for_sql(user_input):
    prompt = f"""
Convert the following user-described symptom into a short clinical keyword phrase suitable for database search.

Examples:
- "ear pain" → "ear infection"
- "burning chest" → "acid reflux"
- "itchy skin" → "allergic reaction"
- "feeling sick" → "nausea"

Input: \"{user_input}\"

Return only the rewritten medical keyword or phrase.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()
