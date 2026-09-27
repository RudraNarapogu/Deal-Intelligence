import sqlite3
import json
from typing import List, Dict, Any, Optional
from backend.config import settings

def get_db():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
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
    CREATE TABLE IF NOT EXISTS outcomes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id TEXT NOT NULL,
        action_taken TEXT NOT NULL,
        result TEXT NOT NULL,
        impact TEXT DEFAULT 'positive',
        notes TEXT DEFAULT '',
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

def add_outcome_db(deal_id: str, action_taken: str, result: str, impact: str = "positive", notes: str = "") -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO outcomes (deal_id, action_taken, result, impact, notes)
    VALUES (?, ?, ?, ?, ?)
    """, (deal_id, action_taken, result, impact, notes))
    outcome_id = cursor.lastrowid

    cursor.execute("UPDATE deals SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (deal_id,))
    conn.commit()
    conn.close()

    return {
        "id": outcome_id,
        "deal_id": deal_id,
        "action_taken": action_taken,
        "result": result,
        "impact": impact,
        "notes": notes
    }

def get_outcomes_db(deal_id: str) -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM outcomes WHERE deal_id = ? ORDER BY id DESC", (deal_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def save_meeting_brief_db(deal_id: str, brief_text: str, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    payload = json.dumps({"meeting_brief": brief_text, "evidence": evidence})
    cursor.execute("""
    INSERT INTO meeting_briefs (deal_id, brief_data)
    VALUES (?, ?)
    """, (deal_id, payload))
    brief_id = cursor.lastrowid

    cursor.execute("UPDATE deals SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (deal_id,))
    conn.commit()
    conn.close()

    return {
        "id": brief_id,
        "deal_id": deal_id,
        "brief_data": payload
    }

def get_meeting_briefs_db(deal_id: str) -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meeting_briefs WHERE deal_id = ? ORDER BY id DESC", (deal_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
