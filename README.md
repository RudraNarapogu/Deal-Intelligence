# 🧠 Deal Intelligence — Hindsight Sales Agent

> **Self-Improving Enterprise Sales Intelligence Agent powered by Hindsight Memory**

Deal Intelligence is a lightweight, modular sales agent built for enterprise deal management. Instead of acting as a traditional CRM, it operates as a strategic intelligence layer for salespeople—tracking customer requirements, objections, stakeholders, and commitments across meetings, and using **Hindsight long-term deal memory** to recommend grounded next steps.

---

## 🌟 Architecture & Core Memory Loop

The system strictly demonstrates the continuous learning loop:

```text
Sales Interaction
        ↓
Hindsight RETAIN  (bank: deal-{id})
        ↓
Persistent Long-Term Memory
        ↓
Hindsight RECALL / REFLECT
        ↓
Grounded LLM Reasoning (Groq gpt-oss-120b)
        ↓
Executive Brief & Action Recommendation
        ↓
Salesperson Action
        ↓
Outcome & Learning Recording
        ↓
Hindsight RETAIN
        ↓
Better Future Decision
```

- **SQLite**: Stores application metadata (deal records, interaction logs, outcome ratings, timestamps).
- **Hindsight Memory Engine**: Long-term deal memory for requirements, objections, pricing, stakeholders, competitors, commitments, decisions, outcomes, and learned information.
- **Groq LLM (`openai/gpt-oss-120b`)**: Grounded reasoning engine synthesising meeting briefs and strategic advice from retrieved Hindsight memory facts.

---

## 🛠️ Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.12, FastAPI, Uvicorn, SQLite (`PRAGMA foreign_keys = ON`)
- **Memory Engine**: Hindsight Cloud / SDK (`hindsight-client`)
- **LLM Engine**: Groq (`openai/gpt-oss-120b`)

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
| ------ | -------- | ------- |
| `GET` | `/api/health` | Real connectivity health check (`api`, `hindsight`, `llm`) |
| `GET` | `/api/deals` | List deal portfolio |
| `POST` | `/api/deals` | Create a deal & initialize Hindsight bank |
| `GET` | `/api/deals/{id}/interactions` | Fetch interaction history |
| `POST` | `/api/deals/{id}/interactions` | Record transcript & run `retain()` into Hindsight |
| `POST` | `/api/deals/{id}/outcomes` | Record salesperson action outcome & retain learning |
| `GET` | `/api/deals/{id}/outcomes` | Fetch recorded deal outcomes |
| `POST` | `/api/deals/{id}/meeting-brief` | Generate grounded executive meeting brief |
| `POST` | `/api/deals/{id}/ask` | Interactive deal Q&A with memory provenance |
| `POST` | `/api/deals/{id}/reflect` | Strategic reflection using Hindsight `areflect()` |
| `GET` | `/api/deals/{id}/memories` | Inspect raw Hindsight bank memories |

---

## 🚀 Quick Start Guide

### 1. Environment Configuration

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

```env
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=sqlite:///./deal_intelligence.db
FRONTEND_URL=http://localhost:5173
VITE_API_BASE_URL=http://localhost:8000/api
```

### 2. Install Dependencies

**Backend:**
```bash
python -m venv venv
.\venv\Scripts\activate   # On Windows
pip install -r backend/requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 3. Run Development Servers

Run the automated launcher script:

```bash
python run_dev.py
```

- **React Dashboard**: [http://localhost:5173](http://localhost:5173)
- **FastAPI Backend**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
