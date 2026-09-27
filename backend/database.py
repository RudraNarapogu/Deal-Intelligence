import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from backend.config import settings

def get_db():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deals (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        client_name TEXT NOT NULL,
        stage TEXT DEFAULT 'Discovery',
        budget TEXT DEFAULT '',
        summary TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id TEXT NOT NULL,
        type TEXT NOT NULL,
        date TEXT NOT NULL,
        title TEXT DEFAULT '',
        transcript TEXT NOT NULL,
        context TEXT DEFAULT 'sales meeting',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (deal_id) REFERENCES deals(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meeting_briefs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id TEXT NOT NULL,
        brief_data TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (deal_id) REFERENCES deals(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hindsight_local_memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id TEXT NOT NULL,
        text TEXT NOT NULL,
        category TEXT DEFAULT 'fact',
        timestamp TEXT,
        metadata TEXT DEFAULT '{}',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# Deal DB helper functions
def list_deals_db() -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deals ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_deal_db(deal_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deals WHERE id = ?", (deal_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_or_update_deal_db(deal_id: str, name: str, client_name: str, stage: str = "Discovery", budget: str = "", summary: str = "") -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO deals (id, name, client_name, stage, budget, summary, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(id) DO UPDATE SET
        name = excluded.name,
        client_name = excluded.client_name,
        stage = excluded.stage,
        budget = excluded.budget,
        summary = excluded.summary,
        updated_at = CURRENT_TIMESTAMP
    """, (deal_id, name, client_name, stage, budget, summary))
    conn.commit()
    conn.close()
    return get_deal_db(deal_id)

def add_interaction_db(deal_id: str, type: str, date: str, title: str, transcript: str, context: str = "sales meeting") -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO interactions (deal_id, type, date, title, transcript, context)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (deal_id, type, date, title, transcript, context))
    interaction_id = cursor.lastrowid

    # Touch deal updated_at
    cursor.execute("UPDATE deals SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (deal_id,))
    conn.commit()
    conn.close()

    return {
        "id": interaction_id,
        "deal_id": deal_id,
        "type": type,
        "date": date,
        "title": title,
        "transcript": transcript,
        "context": context
    }

def get_interactions_db(deal_id: str) -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interactions WHERE deal_id = ? ORDER BY date DESC, id DESC", (deal_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_local_memory_db(deal_id: str, text: str, category: str = "fact", timestamp: str = "") -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO hindsight_local_memories (deal_id, text, category, timestamp)
    VALUES (?, ?, ?, ?)
    """, (deal_id, text, category, timestamp or datetime.utcnow().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()
    return {"deal_id": deal_id, "text": text, "category": category, "timestamp": timestamp}

def get_local_memories_db(deal_id: str) -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hindsight_local_memories WHERE deal_id = ? ORDER BY id DESC", (deal_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
