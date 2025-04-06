import streamlit as st
import os
from dotenv import load_dotenv

# Custom modules
from database.db_connection import run_sql_query
from agents.sql_agent import generate_sql_query
from agents.llm_agent import summarize_medicines

# Load environment variables
load_dotenv()

# Streamlit UI setup
st.set_page_config(page_title="MedXpert", layout="centered")
st.title("💊 MedXpert - AI Powered Medicine Search Assistant")
with st.sidebar:
    st.markdown("### 🔧 Tools")
    st.info("📘 To generate a user manual, select **'User Manual'** from the sidebar menu above.")

       

# Symptom search input
st.subheader("🔎 Search for Medicine by Symptom or Keyword")
user_input = st.text_input("Enter your symptom or keyword (e.g., fever, cold, infection, headache):")

# Helpful caption
st.caption("💡 Try: fever · cough · bacterial · cold · pain · infection · sneezing")

# When user enters something
if user_input:
    try:
        # 🔹 Step 1: Use GPT to generate SQL
        sql_query = generate_sql_query(user_input)

        # 🔍 Show the generated SQL (for debugging/visibility)
        with st.expander("🧠 GPT-Generated SQL Query"):
            st.code(sql_query, language='sql')

        # 🔹 Step 2: Run SQL against the PostgreSQL DB
        columns, rows = run_sql_query(sql_query)

        if rows:
            st.success(f"✅ Found {len(rows)} matching result(s)")
            st.dataframe(rows, use_container_width=True)

            # 🔹 Step 3: Summarize results using GPT-4 (with images embedded)
            with st.spinner("🤖 Summarizing recommended medicines using GPT..."):
                summary_html = summarize_medicines(columns, rows)

            # 🔹 Step 4: Display the final HTML block with names, images & summaries
            st.markdown("### 🧠 GPT Summary with Images")
            st.markdown(summary_html, unsafe_allow_html=True)

            # 🔹 Optional: Download button for text version
            st.download_button("📄 Download Summary", summary_html, file_name="medicine_summary.html")

        else:
            st.warning("❌ No matching medicines found.")
            st.info("💡 Try broader keywords like 'infection', 'cold', or 'pain'.")

    except Exception as e:
        st.error(f"⚠️ An error occurred while processing your request:\n\n{e}")
