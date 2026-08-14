# FINSIGHT-AI

**A Privacy-First RAG-Based Personal Finance Assistant for Bank Statement Analysis**

FINSIGHT-AI lets you upload a bank statement PDF and instantly get a spending dashboard plus a chatbot you can ask natural-language questions about your transactions — all without linking your bank account or storing your data anywhere.

---

## Why FINSIGHT-AI

Most personal finance apps require you to either manually enter every transaction, or link your live bank account through an API — handing over standing access to your financial data. FINSIGHT-AI does neither. It works entirely from a statement you already have, processes everything in memory, and never writes your PDF or transaction data to disk.

It also solves a real problem with AI + finance: LLMs are unreliable at doing math. FINSIGHT-AI never lets the model calculate or state a number on its own — known facts (balance, totals, count) are pre-computed deterministically, and open-ended numeric questions are answered by having the LLM generate code that gets *executed*, not guessed.

---

## Features

- 📄 **Automatic PDF extraction** — dual-strategy table extraction (line-based + text-based), no manual data entry
- 🔒 **Privacy by design** — nothing is ever written to disk; entire session lives in memory
- 📊 **Instant dashboard** — total income/expense, category breakdown, monthly trend, top merchants (pure pandas, zero AI involved)
- 💬 **Conversational chatbot** — ask things like *"how much did I spend on food"* or *"what's my current balance"*
- 🧠 **Hybrid RAG architecture** — deterministic facts first → generated & executed code → semantic search fallback, in that order
- 🏷️ **Smart categorization** — rule-based merchant matching first, LLM fallback only for what rules can't catch

---

## Architecture

```
PDF Upload → Table Extraction → Row Filtering → Schema Cleaning → Categorization
                                                                        ↓
                                                            Master DataFrame
                                                          (session-only, in-memory)
                                                          /                    \
                                            Dashboard Engine              Chat Engine
                                            (pure pandas, no LLM)          (Hybrid RAG)
```

**Chat engine query flow:**
```
User Question → Check Known Facts (statement_info)
              → Generate & Execute Pandas Code
              → Semantic Search (if no result)
              → LLM Synthesis (phrases final answer)
```

---

## Tech Stack

| Purpose | Tool |
|---|---|
| Package/env manager | [uv](https://github.com/astral-sh/uv) |
| Frontend + backend | Streamlit |
| PDF extraction | pdfplumber |
| Data handling | pandas |
| Vector database | ChromaDB |
| Embedding model | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | Groq API (llama-3.3-70b-versatile) |

---

## Project Structure

```
FINSIGHT-AI/
├── backend/
│   ├── config.py          # constants, category keywords
│   ├── schemas.py         # fixed transaction schema
│   ├── pdf_parser.py      # PDF → table extraction
│   ├── pii_mask.py        # narration PII scrubbing
│   ├── extractor.py       # rows → structured transactions
│   ├── cleaner.py         # schema validation, dedupe
│   ├── categorizer.py     # rule-based + LLM categorization
│   ├── embeddings.py      # ChromaDB embedding + search
│   ├── rag.py             # chat engine logic
│   ├── llm.py             # Groq API entry point
│   ├── dashboard.py       # pandas aggregations
│   └── utils.py           # shared helpers
├── frontend/
│   ├── upload.py
│   ├── dashboard.py
│   ├── chatbot.py
│   └── components.py
├── data/chroma_db/         # persisted vector index only
├── app.py                   # entry point
├── .env                      # GROQ_API_KEY (not committed)
├── pyproject.toml
└── uv.lock
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) installed
- A free [Groq API key](https://console.groq.com)

### Setup

```bash
git clone https://github.com/<your-username>/FINSIGHT-AI.git
cd FINSIGHT-AI

uv sync
```

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_key_here
```

### Run

```bash
uv run streamlit run app.py
```

Open the local URL Streamlit prints in your browser, upload a bank statement PDF, and explore the dashboard and chatbot.

---

## Current Scope

- Supports text-based PDF statements (Kotak Mahindra Bank format tested)
- Single statement per session, no cross-session history
- Max upload size: 1MB

## Roadmap

- [ ] Multi-bank format support
- [ ] OCR support for scanned statements
- [ ] Multi-statement / month-over-month comparison
- [ ] Recurring payment detection
- [ ] Budget alerts
- [ ] Local LLM inference (remove external API dependency)

---

## License

This project was built as an academic project. Add a license of your choice here (e.g., MIT) before public distribution.