import streamlit as st
import os
from dotenv import load_dotenv

# Custom modules
from database.db_connection import run_sql_query
from agents.sql_agent import generate_sql_query
from agents.llm_agent import summarize_medicines

# Load environment variables
load_dotenv()

# ✅ Streamlit UI setup
st.set_page_config(page_title="MedXpert", layout="centered")

# ✅ App Title
st.title("💊 MedXpert - AI Powered Medicine Search Assistant")

# ✅ Sidebar Navigation
with st.sidebar:
    st.markdown("### 🔧 Tools")
    st.markdown("📘 Use the sidebar above to navigate to the **User Manual** generator.")

# ✅ Symptom Search Input
st.subheader("🔎 Search for Medicine by Symptom or Keyword")
user_input = st.text_input("Enter your symptom or keyword (e.g., fever, cold, infection, headache):")

# ✅ Helpful Caption
st.caption("💡 Try: fever · cough · bacterial · cold · pain · infection · sneezing")

# ✅ Process on User Input
if user_input:
    try:
        # 🔹 Step 1: Generate SQL using GPT
        sql_query = generate_sql_query(user_input)

        # 🔍 Show Generated SQL
        with st.expander("🧠 GPT-Generated SQL Query"):
            st.code(sql_query, language='sql')

        # 🔹 Step 2: Execute SQL Query
        columns, rows = run_sql_query(sql_query)

        # 🔹 Step 3: Handle Query Results
        if rows:
            st.success(f"✅ Found {len(rows)} matching result(s)")
            st.dataframe(rows, use_container_width=True)

            with st.spinner("🤖 Summarizing recommended medicines using GPT..."):
                summary_html = summarize_medicines(columns, rows)

            # 🔹 Step 4: Display Summary with Custom Heading
            st.markdown("### 💡 MedXpert_LLMAgent Summaries")
            st.markdown(summary_html, unsafe_allow_html=True)

            # 🔹 Optional: Download Button
            st.download_button("📄 Download Summary", summary_html, file_name="medicine_summary.html")
        else:
            st.warning("❌ No matching medicines found.")
            st.info("💡 Try broader keywords like 'infection', 'cold', or 'pain'.")

    except Exception as e:
        st.error(f"⚠️ An error occurred while processing your request:\n\n{e}")
