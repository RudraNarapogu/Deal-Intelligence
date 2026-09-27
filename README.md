# 🧠 Deal Intelligence — Hindsight Sales Agent

> **Self-Improving Enterprise Sales Intelligence Agent powered by Hindsight Memory**

Deal Intelligence is a lightweight, modular sales agent built for enterprise deal management. Instead of acting as a traditional CRM, it operates as a strategic intelligence layer for salespeople—tracking customer requirements, objections, stakeholders, and commitments across meetings, and using **Hindsight long-term deal memory** to recommend actionable next steps.

---

## 🌟 Key Features

1. **Dedicated Hindsight Memory Banks (`deal-{id}`)**:
   - Isolates each client's history into a clean, dedicated Hindsight memory bank (`deal-acme-corp`, `deal-zenith-ltd`, `deal-nova-systems`).
2. **Automated Memory Extraction (`retain`)**:
   - Processes raw meeting transcripts into structured facts, objections, entity graphs, temporal notes, and outcome learnings.
3. **Hybrid RAG Memory Retrieval (`recall`)**:
   - Combines semantic similarity, keyword search, entity graphs, and temporal retrieval to fetch relevant deal context.
4. **Executive Meeting Preparation Briefs**:
   - Automatically synthesizes deal status, key requirements, unresolved objections, competitor intelligence, and recommended meeting priorities.
5. **Visible Hindsight Memory Evidence**:
   - Transparently highlights the exact historical memories that informed the agent's recommendations.
6. **Continuous Learning Loop**:
   - Retains meeting outcomes (what pitches succeeded or failed) so future recommendations adapt based on past results.

---

## 🏗️ Architecture

```text
                    SALESPERSON
                         │
                         ▼
                ┌────────────────┐
                │ React Dashboard│
                └───────┬────────┘
                        │
                        ▼
                ┌────────────────┐
                │ FastAPI Agent  │
                │ Orchestrator   │
                └───────┬────────┘
                        │
              ┌─────────┴──────────┐
              │                    │
              ▼                    ▼
       ┌──────────────┐     ┌──────────────┐
       │  Hindsight   │     │  Groq LLM    │
       │  Memory Bank │     │ (gpt-oss /   │
       │  RETAIN      │     │  Llama-3.3)  │
       │  RECALL      │     │              │
       │  REFLECT     │     │ Reasoning    │
       └──────┬───────┘     └──────┬───────┘
              │                    │
              └─────────┬──────────┘
                        ▼
                 DEAL INTELLIGENCE
```

---

## 🛠️ Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.12, FastAPI, Uvicorn, SQLite
- **Memory Engine**: Hindsight Cloud / SDK (`hindsight-client`)
- **LLM Engine**: Groq (`llama-3.3-70b-versatile`)

---

## 🚀 Quick Start Guide

### 1. Clone & Setup Environment

```bash
git clone https://github.com/RudraNarapogu/Deal-Intelligence.git
cd Deal-Intelligence
```

### 2. Configure `.env`

Create a `.env` file in the root directory:

```env
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=sqlite:///./deal_intelligence.db
```

### 3. Install Dependencies

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

### 4. Run Development Servers

Run the automated launcher script:

```bash
python run_dev.py
```

- **React Dashboard**: [http://localhost:5173](http://localhost:5173)
- **FastAPI Backend**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
