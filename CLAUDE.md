# CLAUDE.md - AI Assistant Guide for MedXpert

This document provides essential context for AI assistants working on the MedXpert codebase.

## Project Overview

**MedXpert** is a multi-agent, LLM-powered medical chatbot that transforms natural language symptom queries into structured insights, multilingual medicine summaries, and interactive dashboards. It combines SQL-based structured search with vector-based semantic search to provide comprehensive medicine recommendations.

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main application
streamlit run app.py

# Run vector search test app
streamlit run qdrant_search_app.py
```

**Required Environment Variables** (create `.env` file):
```
OPENAI_API_KEY=your_key_here
```

## Project Structure

```
medxpert/
├── app.py                          # Main Streamlit entry point
├── agents/                         # AI agent modules
│   ├── __init__.py
│   ├── llm_agent.py               # LLM functions: classification, summarization, chat
│   └── sql_agent.py               # SQL query generation via GPT-4
├── modules/                        # Utility modules
│   └── user_manual_generator.py   # Multilingual manual generation
├── pages/                          # Streamlit multi-page components
│   └── 1_User_Manual.py           # User manual generation page
├── database/                       # Database connection (gitignored)
│   └── db_connection.py           # PostgreSQL connection & query execution
├── build_qdrant.py                # Vector store initialization
├── dailymed_ingest_qdrant.py      # DailyMed data ingestion pipeline
├── qdrant_search_app.py           # Semantic search test application
├── chroma_test_app.py             # ChromaDB vector search test
├── vector_test.py                 # Vector database testing
├── ocr_to_fields.py               # OCR prescription extraction
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## Architecture

```
User Input (symptoms)
       ↓
Intent Classification (GPT-4)
    ↙         ↘
SQL Agent    Vector Agent
    ↘         ↙
 Aggregated LLM Summary
       ↓
 Multilingual Explanation
       ↓
 Ratings Visualization
```

### Core Components

1. **Intent Classifier** (`agents/llm_agent.py:classify_input_type`) - Determines if input is `general_chat` or `symptom_query`
2. **SQL Agent** (`agents/sql_agent.py:generate_sql_query`) - Generates PostgreSQL queries from natural language
3. **LLM Summarizer** (`agents/llm_agent.py:summarize_medicines`) - Creates patient-friendly medicine summaries
4. **Manual Generator** (`modules/user_manual_generator.py`) - Produces multilingual user manuals

## Technology Stack

| Category | Technologies |
|----------|-------------|
| LLM | OpenAI GPT-4, GPT-3.5-turbo |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2, 384-dim) |
| Vector DB | Qdrant (primary), ChromaDB (secondary) |
| Relational DB | PostgreSQL with SQLAlchemy |
| Frontend | Streamlit |
| Translation | Google Translate (googletrans) |
| Visualization | Matplotlib |
| PDF Generation | ReportLab |

## Database Schema

The primary table `medicines_table` has these columns (case-sensitive):
- `Medicine_Name` - Name of the medicine
- `Composition` - Dosage/composition information
- `Uses` - Medical uses and indications
- `Side_effects` - Known side effects
- `Image_URL` - URL to medicine image
- `Manufacturer` - Manufacturing company
- `Excellent_Review_Percent` - Positive review percentage
- `Average_Review_Percent` - Average review percentage
- `Poor_Review_Percent` - Poor review percentage

## Code Conventions

### File Organization
- **agents/**: Contains AI/ML pipeline components (LLM agents, SQL agents)
- **modules/**: Contains reusable utility functions
- **pages/**: Contains Streamlit multi-page UI components (numbered for ordering)

### Naming Conventions
- Functions: `snake_case` (e.g., `generate_sql_query`, `summarize_medicines`)
- Files: `lowercase_with_underscores.py`
- Variables: Descriptive names with context

### Comment Style
- Emoji prefixes are used in comments for readability (e.g., `# 🔹 General chat`)
- Docstrings for main functions with parameter descriptions

### OpenAI API Usage
Two patterns are used in the codebase:

**New client pattern** (preferred, in `agents/`):
```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-4",
    messages=[...]
)
```

**Legacy pattern** (in `modules/`):
```python
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[...]
)
```

### Streamlit Patterns
- Session state for chat history: `st.session_state.chat_history`
- HTML/CSS styling via `st.markdown(..., unsafe_allow_html=True)`
- Sidebar for navigation and settings
- Expanders for showing generated SQL queries

## Key Functions Reference

### agents/llm_agent.py
| Function | Purpose | Model |
|----------|---------|-------|
| `chat_with_user(user_input)` | General conversation | GPT-3.5-turbo |
| `summarize_medicines(columns, rows)` | Medicine summaries with HTML | GPT-4 |
| `classify_input_type(user_input)` | Intent classification | GPT-4 |
| `generate_general_reply(user_input)` | Friendly responses | GPT-4 |
| `rephrase_symptom_for_sql(user_input)` | Symptom to keywords | GPT-4 |

### agents/sql_agent.py
| Function | Purpose | Model |
|----------|---------|-------|
| `generate_sql_query(user_input, table_name)` | Dynamic SQL generation | GPT-4 |

### modules/user_manual_generator.py
| Function | Purpose | Model |
|----------|---------|-------|
| `generate_user_manual(medicine_details, language)` | Multilingual manuals | GPT-4 |

## Common Development Tasks

### Adding a New Agent
1. Create a new file in `agents/` directory
2. Import OpenAI client using the new pattern
3. Define functions with clear docstrings
4. Add emoji-prefixed comments for sections

### Adding a New Streamlit Page
1. Create a new file in `pages/` with numeric prefix (e.g., `2_New_Feature.py`)
2. Follow existing page structure with styled headers
3. Add navigation option in `app.py` sidebar if needed

### Modifying Database Queries
1. SQL generation happens in `agents/sql_agent.py`
2. Queries are generated via GPT-4 prompts
3. Column names are case-sensitive (use exact names from schema)
4. Always sort by `Excellent_Review_Percent DESC` and limit results

### Testing Vector Search
- Use `qdrant_search_app.py` for Qdrant testing
- Use `chroma_test_app.py` for ChromaDB testing
- Qdrant server expected at `localhost:6333`

## External Dependencies

### Required Services
- **PostgreSQL**: Must be running with `medicines_table` populated
- **Qdrant** (optional): Vector database at `localhost:6333`
- **OpenAI API**: Valid API key required

### Data Sources
- [DailyMed Structured Product Labels](https://dailymed.nlm.nih.gov/dailymed/)
- Kaggle 11K+ medicine dataset

## Files Not in Repository

The following are gitignored and must be configured locally:
- `.env` - Environment variables including API keys
- `database/` - Database connection module
- `data/`, `output/`, `outputs/` - Generated data directories
- `qdrant_data/`, `chroma_db_fresh/` - Vector database storage
- `*.csv`, `*.json` - Data files

## Important Notes for AI Assistants

1. **Database module not in repo**: The `database/db_connection.py` is gitignored. When suggesting database changes, note that users need to implement their own connection logic.

2. **API version differences**: The codebase uses `openai==0.28.1` which has different syntax from newer versions. Some files use the new client pattern, others use the legacy pattern.

3. **Case-sensitive columns**: PostgreSQL column names must match exactly (e.g., `Medicine_Name`, not `medicine_name`).

4. **HTML in Streamlit**: Medicine summaries return HTML that's rendered via `unsafe_allow_html=True`.

5. **Session state management**: Chat history persists in `st.session_state.chat_history`.

6. **Error handling**: Wrap OpenAI API calls in try-except blocks to handle rate limits and errors gracefully.

7. **Prompt engineering**: SQL and classification prompts include specific instructions to avoid markdown formatting in responses.

## Testing Checklist

Before committing changes:
- [ ] Verify Streamlit app starts without errors
- [ ] Test intent classification with both chat and symptom inputs
- [ ] Confirm SQL queries execute correctly (if database available)
- [ ] Check that HTML rendering works in medicine summaries
- [ ] Validate any new prompts return expected formats

## Contributors

- **Krishna Annavaram** - Primary developer
- **Vighnasree Vara** - NLP & GenAI Research Collaborator

## License

MIT License - See LICENSE file for details.
