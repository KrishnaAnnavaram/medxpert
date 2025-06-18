import streamlit as st
import os
from dotenv import load_dotenv

# Custom modules
from database.db_connection import run_sql_query
from agents.sql_agent import generate_sql_query
from agents.llm_agent import summarize_medicines, classify_input_type, generate_general_reply, rephrase_symptom_for_sql

# Load environment variables
load_dotenv()

# Set up Streamlit page
st.set_page_config(page_title="💊 MedXpert - AI Medicine Assistant", layout="centered")

# 🎨 Sidebar Styling
st.sidebar.markdown("<style>div[data-testid='stSidebar'] {background-color: #D0E2F2;}</style>", unsafe_allow_html=True)

# 🎯 Pages
selected_page = st.sidebar.radio("📚 Pages", ["Home", "User Manual", "About MedXpert"])

# 📢 Sidebar Announcements
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📢 Announcements")
    st.info("🚀 MedXpert Phase 1 Completed! Coming Soon: Audio Input/Output + Multilingual Support!")
    st.markdown("---")
    st.caption("👨‍⚕️ Powered by Krishna Annavaram & Vighnasree Vara.")

# Footer Text
footer_text = "© 2025 Krishna Annavaram and Vighnasree Vara. All rights reserved."

# 🏠 Home Page
if selected_page == "Home":
    st.markdown("""
    <h1 style='text-align: center; font-size: 36px; color: #0066cc;'>👩‍⚕️ MedXpert - Your AI Medicine Guide</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<h4 style='font-size: 20px;'>🗣️ Start a conversation with MedXpert:</h4>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"🧑‍💻 **Patient:** {msg['content']}")
        else:
            with st.chat_message("assistant"):
                st.markdown(f"👩‍⚕️ **MedXpert Assistant:**\n\n{msg['content']}", unsafe_allow_html=True)

    user_input = st.chat_input("💬 Talk to MedXpert (symptoms, general advice, or greetings!)")

    if user_input:
        with st.spinner('🔄 MedXpert is thinking...'):
            # Save User Message First
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            try:
                input_type = classify_input_type(user_input)

                if input_type == "general_chat":
                    reply = generate_general_reply(user_input)

                elif input_type == "symptom_query":
                    rephrased_input = rephrase_symptom_for_sql(user_input)
                    st.caption(f"🧠 Interpreted Symptom: {rephrased_input}")

                    sql_query = generate_sql_query(rephrased_input)

                    with st.expander("🧠 Click to view SQL Agent Generated Query"):
                        st.code(sql_query, language="sql")

                    columns, rows = run_sql_query(sql_query)

                    if rows:
                        summary_html = summarize_medicines(columns, rows)
                        reply = f"### 🧠 MedXpert Recommendations\n{summary_html}"

                        # Optional: Plot Graph
                        import pandas as pd
                        import matplotlib.pyplot as plt
                        try:
                            df = pd.DataFrame(rows, columns=columns)
                            if 'Excellent_Review_Percent' in df.columns and 'Medicine_Name' in df.columns:
                                st.markdown("### 📊 Medicine Ratings Overview:")
                                fig, ax = plt.subplots(figsize=(12, 6))
                                meds = df['Medicine_Name']
                                ratings = df['Excellent_Review_Percent'].astype(float)
                                ax.bar(meds, ratings, color='#4CAF50', edgecolor='black')
                                ax.set_title('Medicine vs Excellent Review %', fontsize=18)
                                ax.set_xlabel('Medicine Name', fontsize=14)
                                ax.set_ylabel('Excellent Review %', fontsize=14)
                                ax.grid(axis='y', linestyle='--', alpha=0.7)
                                plt.xticks(rotation=45, ha='right')
                                st.pyplot(fig)
                        except Exception as viz_err:
                            st.warning(f"Visualization skipped: {viz_err}")

                    else:
                        reply = ("⚠️ No matching medicines found.\n\n"
                                 "💡 Try broader symptoms like 'pain', 'cold', or 'infection'.")

                else:
                    reply = "⚠️ Sorry, I couldn't understand your query properly. Please rephrase."

            except Exception as e:
                reply = f"⚠️ Error: {e}"

            # ✅ Always Save Assistant's Message
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

            # ✅ Display Assistant's Message
            with st.chat_message("assistant"):
                st.markdown(reply, unsafe_allow_html=True)

    # Sidebar Clear Button
    with st.sidebar:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.experimental_rerun()

    st.markdown("---")
    st.caption(footer_text)

# 📄 User Manual Page
elif selected_page == "User Manual":
    st.markdown("""
    <h2 style='color: #0066cc;'>📖 How to Use MedXpert</h2>
    """, unsafe_allow_html=True)
    st.write("""
    - 🧑‍💻 Type your medical symptoms (e.g., 'fever', 'cough', 'infection') in the chat box.
    - 🧠 MedXpert intelligently interprets symptoms and suggests medicines.
    - 💬 You can casually chat too — not only symptoms!
    - 🧾 SQL database lookup and GPT summarization happen automatically.
    - 🖼 Medicines shown with name, composition, uses, side effects.
    - 📊 Ratings chart displayed if multiple medicines found.
    - 🗑️ Sidebar button to clear chat history anytime.
    """)
    st.markdown("---")
    st.caption(footer_text)

# 📄 About MedXpert Page
elif selected_page == "About MedXpert":
    st.markdown("""
    <h2 style='color: #0066cc;'>👩‍⚕️ About MedXpert</h2>
    """, unsafe_allow_html=True)
    st.write("""
    MedXpert is an intelligent AI-driven assistant built to:
    - Recommend medicines based on user symptoms.
    - Summarize medical data in an easy-to-understand format.
    - Help users make faster and smarter healthcare decisions.

    **Built By:**  
    👨‍💻 Krishna Annavaram  
    👩‍💻 Vighnasree Vara  
    """)
    st.markdown("---")
    st.caption(footer_text)
