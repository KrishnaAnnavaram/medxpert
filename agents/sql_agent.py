import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_sql_query(user_input, table_name="medicines_table"):
    """
    Generates a SQL query based on user input using GPT-4.
    It searches 'Uses', 'Medicine_Name', and 'Composition' columns
    and sorts by Excellent_Review_Percent.
    """
    prompt = f"""
You are a PostgreSQL SQL query generator for a medical chatbot.

Table: {table_name}

Here are the actual column names (case-sensitive):
- "Medicine_Name"
- "Composition"
- "Uses"
- "Side_effects"
- "Image_URL"
- "Manufacturer"
- "Excellent_Review_Percent"
- "Average_Review_Percent"
- "Poor_Review_Percent"

User entered: "{user_input}"

1. First, identify all synonyms and medically relevant terms related to the input (e.g., fever → high temperature, viral infection).
2. Then, write a SQL query that searches "Uses", "Medicine_Name", or "Composition" for any of those using ILIKE.
3. Sort by "Excellent_Review_Percent" DESC.
4. Limit to 3 rows.
5. ❗️Output ONLY the raw SQL query. Do NOT add:
   - Markdown (like ```sql)
   - Comments or explanations
   - Any extra text
Just return valid SQL that can be executed directly.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You generate safe SQL queries for PostgreSQL medical databases."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
