# 💊 MedXpert – Multilingual GenAI-Powered Medical Assistant

**MedXpert** is a multi-agent, LLM-powered medical chatbot that transforms natural language symptom queries into structured insights, multilingual medicine summaries, and interactive dashboards using real-time SQL + vector search.

Built with a modular, secure, and production-scalable architecture, MedXpert blends cutting-edge GenAI (GPT-4), RAG systems, and multilingual NLP to assist patients, researchers, and clinicians in navigating medicine information.

---

## 🚀 Key Features

- 🧠 **Symptom Understanding** via Module Context Protocol (MCP)
- 📂 **SQL Agent**: GPT-4 powered dynamic query generator for structured databases
- 🔎 **Vector Agent**: ChromaDB + MiniLM for semantic similarity over medical content
- 📄 **LLM Summarizer**: Generates patient-level, multilingual medicine descriptions
- 🌐 **Manual Generator**: 100+ language support using MarianMT + Prompt Engineering
- 🧾 **OCR-Based Input**: Read prescriptions using Tesseract OCR + NER
- 📊 **Rating Visualization**: Auto-generated medicine performance charts
- 🔒 **Clean Architecture**: Modular components and optional HIPAA-safe deployment

---

## 🛠️ Tech Stack

| Layer              | Stack                                                                 |
|-------------------|-----------------------------------------------------------------------|
| LLM                | GPT-4 (OpenAI), LangChain-style Agents, SentenceTransformers (MiniLM) |
| NLP + Search       | TF-IDF, Cosine Similarity, ChromaDB, Vector Indexing                  |
| Multilingual NLP   | MarianMT, HuggingFace Transformers, spaCy                            |
| Data & BI          | PostgreSQL, Power BI, Matplotlib                                      |
| Frontend           | Streamlit                                                             |
| Deployment         | Docker (Optional), Azure, GCP App Engine                              |
| Other Tools        | GitHub Actions, FastAPI, Tesseract OCR, MLflow, Jira, SharePoint      |

---

## 🧠 Architecture Highlights

```
🧑 User Input (symptoms)
     ⬇
🧠 MCP → Classify intent
     ↙           ↘
SQL Agent     Vector Agent
     ↘           ↙
      Aggregated LLM Summary
               ↓
      📄 Multilingual Explanation
               ↓
      📊 Ratings + Visualizations
```

---

## 🔗 Dataset Sources

- [DailyMed Structured Product Labels](https://dailymed.nlm.nih.gov/dailymed/)
- Kaggle 11K+ medicine info
- Custom labeled translations (MarianMT + Post-processing)

---

## 📂 Project Structure

```
medxpert/
├── agents/              # SQL, LLM, and Vector agents
├── modules/             # Manual generation, utils
├── pages/               # Streamlit multi-page UI
├── app.py               # Main entrypoint
├── build_qdrant.py      # Vector store setup
├── database/            # PostgreSQL structure (ignored)
├── requirements.txt     # Dependencies
├── .gitignore           # Ignore large files
└── README.md            # You're here!
```

---

## 🧪 How to Run

```bash
git clone https://github.com/KrishnaAnnavaram/medxpert.git
cd medxpert
pip install -r requirements.txt
streamlit run app.py
```

Requires `.env` file with:

```
OPENAI_API_KEY=your_key_here
```

---

## 📖 Example Use Cases

- 🤒 “What to take for sore throat?” → GPT-4 → SQL → PostgreSQL
- 🌍 “Tell me about this medicine in Telugu” → MarianMT → User Manual
- 📷 Upload prescription → Tesseract OCR → NLP pipeline
- 📊 Get best-rated alternatives → Chart output by Streamlit

---

## 🧑‍💻 Contributors

- **Krishna Annavaram**  
  [LinkedIn](https://www.linkedin.com/in/krishna-annavaram) | [annavaramkrishna02@gmail.com](mailto:annavaramkrishna02@gmail.com)

- **Vighnasree Vara**  
  NLP & GenAI Research Collaborator

---

## 📜 License

[MIT License](LICENSE)

---

## 🙌 Acknowledgments

Thanks to the University of North Texas – College of Information for academic and technical mentorship in LLM-based AI systems.  
Special appreciation to the GenAI & NLP teams at Creative Sense Pvt Ltd for enabling healthcare RAG system deployment.

---
