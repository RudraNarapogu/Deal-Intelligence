# 🧠 Deal Intelligence — Hindsight Sales Memory Agent

> **Self-Improving Enterprise Sales Intelligence Agent powered by Hindsight Long-Term Memory & Groq LLM**

**Author & Developer**: **Rudra Narapogu**  
**Repository**: [https://github.com/RudraNarapogu/Deal-Intelligence](https://github.com/RudraNarapogu/Deal-Intelligence)  
**Hackathon Target**: Hindsight Memory AI Agent Challenge

---

## 📌 Executive Overview

**Deal Intelligence** is a lightweight, modular AI agent system engineered specifically for enterprise B2B sales teams. Rather than acting as a passive CRM record store, Deal Intelligence functions as an active strategic advisor for salespeople—tracking how customer requirements, objections, budgets, stakeholders, and commitments evolve across months of complex sales conversations.

By utilizing **Hindsight Memory Banks** (`deal-{id}`), the agent maintains persistent, un-corrupted long-term deal context across dozens of meetings. It uses **Hindsight `arecall` and `areflect`** combined with **Groq `openai/gpt-oss-120b`** to generate grounded executive meeting briefs, answer complex deal queries, and learn continuously from past sales approach outcomes.

---

## 🌟 The Continuous Memory & Learning Loop

The system operates on a 6-stage continuous learning architecture:

```text
Sales Interaction / Meeting Transcript
                 ↓
      Hindsight RETAIN  (bank: deal-{id})
                 ↓
     Persistent Long-Term Deal Memory
                 ↓
    Hindsight RECALL / REFLECT  (hybrid RAG)
                 ↓
  Grounded Reasoning  (Groq openai/gpt-oss-120b)
                 ↓
    Executive Meeting Brief & Next Action
                 ↓
           Salesperson Action
                 ↓
   Recorded Outcome & Strategic Learning
                 ↓
      Hindsight RETAIN  (outcome memory)
                 ↓
     Improved Future Sales Recommendations
```

### Key Architectural Principles
1. **One Bank Per Deal**: Every deal (`acme-corp`, `zenith-ltd`, `nova-systems`) receives its own isolated Hindsight memory bank (`deal-acme-corp`), guaranteeing zero cross-customer data leakage.
2. **SQLite for Metadata, Hindsight for Memory**: SQLite manages application metadata (deal records, interaction logs, outcome ratings). Hindsight handles long-term memory extraction, entity graphs, temporal tracking, and factual recall.
3. **Strict Grounded RAG (Zero Hallucination)**: The AI agent uses retrieved Hindsight memories as its sole source of customer facts. It never fabricates pricing, stakeholders, or objections.
4. **Outcome Learning Feedback Loop**: Salespeople record explicit outcomes (`action_taken`, `result`, `impact`), which are retained in Hindsight to train future strategic advice.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.12, FastAPI, Uvicorn, SQLite (`PRAGMA foreign_keys = ON`)
- **Memory Engine**: Hindsight Cloud SDK (`hindsight-client`)
- **LLM Engine**: Groq API (`openai/gpt-oss-120b` / `qwen/qwen3.8-27b`)
- **Testing & Dataset**: Pytest/TestClient E2E assertion suite + 50-interaction longitudinal dataset generator

---

## 📊 Synthetic Longitudinal Stress-Testing Dataset

The repository includes a dedicated dataset generator script (`scripts/generate_test_interactions.py`) that generates **50 chronological interactions** across two distinct companies:

1. **Acme Corporation (`acme-corp`)**:
   - **Use Case**: Invoice Automation Platform (10,000 monthly invoices).
   - **Evolution**: 25 chronological interactions spanning 7 months (`2026-03-01` to `2026-09-28`).
   - **Storyline**: Initial discovery -> SAP ECC 6.0 REST API requirements -> CSO David Vance security objection (multi-tenant cloud isolation & SOC2) -> CFO Thomas Wright Q4 timeline constraint (10-day deployment) -> Competitor InvoiceFlow (₹70k) evaluation -> Budget reduction (₹120k down to ₹80k) -> SOC2 whitepaper delivery & deal closed won at ₹80,000.

2. **Zenith Logistics (`zenith-ltd`)**:
   - **Use Case**: Fleet Management & Route Optimization (500 delivery trucks).
   - **Evolution**: 25 chronological interactions spanning 7.5 months (`2026-02-15` to `2026-09-25`).
   - **Storyline**: Manual tracking & ₹3,50,000 fuel waste -> OBD-II telematics & driver Android app specs -> Mandatory offline mobile sync requirement -> Driver adoption objection -> Maintenance Manager Vikram Patel engine telemetry focus -> Competitor FleetTrack Pro (₹140k smartphone GPS) -> Budget reduction (₹200k down to ₹150k) -> Live rural blackout offline sync proof -> 2-year contract closed won at ₹150,000.

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET` | `/api/health` | Real connectivity health check (`api`, `hindsight`, `llm`) |
| `GET` | `/api/deals` | List all deals in portfolio |
| `POST` | `/api/deals` | Create a new deal & initialize its Hindsight memory bank |
| `GET` | `/api/deals/{id}/interactions` | List recorded interaction transcripts |
| `POST` | `/api/deals/{id}/interactions` | Record meeting transcript & run Hindsight `retain()` |
| `POST` | `/api/deals/{id}/outcomes` | Record salesperson action outcome & retain learning |
| `GET` | `/api/deals/{id}/outcomes` | List recorded outcomes for deal |
| `POST` | `/api/deals/{id}/meeting-brief` | Generate executive meeting brief using Hindsight memory & Groq |
| `POST` | `/api/deals/{id}/ask` | Interactive Q&A chat with memory provenance citations |
| `POST` | `/api/deals/{id}/reflect` | High-level strategic reflection using Hindsight `areflect()` |
| `GET` | `/api/deals/{id}/memories` | Inspect raw Hindsight bank memory facts & entity graph |

---

## 🚀 How to Setup and Run Locally

### 1. Prerequisites
- **Python**: Version 3.10+
- **Node.js**: Version 18+ and `npm`

### 2. Environment Configuration (`.env`)

Copy `.env.example` to `.env` in the root directory:

```bash
cp .env.example .env
```

Set your API keys in `.env`:

```env
# Hindsight Memory Engine Credentials
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io

# Groq LLM API Credentials
GROQ_API_KEY=your_groq_api_key

# Application & Network Settings
DATABASE_PATH=deal_intelligence.db
FRONTEND_URL=http://localhost:5173
VITE_API_BASE_URL=http://localhost:8000/api
```

### 3. Backend Setup

```bash
# Initialize virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 5. Run the Application

You can launch both the **FastAPI Backend** and **React Frontend** together using the launcher script:

```bash
python run_dev.py
```

Or start them in separate terminals:

**Terminal 1 (Backend):**
```bash
.\venv\Scripts\python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### 6. Ingest Synthetic Longitudinal Stress-Testing Dataset

To ingest the 50-interaction dataset through the real application flow:

```bash
# Test dataset structure without sending HTTP requests
python scripts/generate_test_interactions.py --dry-run

# Ingest all 50 interactions via real FastAPI backend endpoints
python scripts/generate_test_interactions.py
```

### 7. Run Test & Compilation Validation Suite

```bash
# Python bytecode compilation check
python -m compileall -q backend

# Run E2E assertion smoke test suite
python test_hardened_system.py

# Verify frontend production build
cd frontend
npm run build
```

---

## 👤 Author Credentials & Submission Information

- **Developer**: **Rudra Narapogu**
- **Email**: `rudranarapogu@gmail.com`
- **GitHub Repository**: [https://github.com/RudraNarapogu/Deal-Intelligence](https://github.com/RudraNarapogu/Deal-Intelligence)
- **Project**: Deal Intelligence — Hindsight-powered AI Sales Agent
