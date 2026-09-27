import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from backend.services.hindsight_service import hindsight_service
from backend.services.llm_service import llm_service
from backend.database import (
    get_deal_db,
    add_interaction_db,
    add_outcome_db,
    get_outcomes_db,
    get_interactions_db
)

logger = logging.getLogger("deal_intelligence.agent")
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

def load_prompt(filename: str) -> str:
    path = PROMPTS_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "You are an enterprise sales intelligence agent."

def strip_uuid_citations(text: str) -> str:
    """
    Remove raw memory UUIDs, bracketed citations (e.g. 【id】), and experience/world IDs from text output
    to present clean, executive-ready Markdown.
    """
    if not text:
        return ""
    text = re.sub(r'【[^】]*】', '', text)
    text = re.sub(r'\(?\b(experience|observation|world|ID:?)\s*[a-f0-9\-]{36}\)?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\(\s*\)', '', text)
    text = re.sub(r' +\.', '.', text)
    text = re.sub(r' +,', ',', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

class DealAgent:
    def normalize_recall_context(self, recall_data: Dict[str, Any]) -> str:
        """
        Normalize raw Hindsight recall JSON into clean, structured Markdown context.
        Groups facts by timestamp and memory category.
        """
        results = recall_data.get("results") or recall_data.get("facts") or recall_data.get("memories") or []
        if not results or not isinstance(results, list):
            return "No historical memories currently stored in Hindsight bank."

        lines = ["### RETRIEVED HINDSIGHT DEAL MEMORIES:"]
        for idx, item in enumerate(results[:20]):
            if isinstance(item, dict):
                text = item.get("text") or item.get("content") or item.get("fact") or str(item)
                ts = item.get("timestamp") or item.get("created_at") or item.get("date") or "Retained Memory"
                mem_type = item.get("type") or item.get("category") or "Fact"
                mem_id = item.get("id") or f"mem-{idx+1}"
                lines.append(f"- **[{ts}] ({mem_type})**: {text}")
            elif isinstance(item, str):
                lines.append(f"- **(Fact)**: {item}")

        return "\n".join(lines)

    def extract_evidence_from_recall(self, recall_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract clean, human-readable provenance items from Hindsight recall response.
        """
        evidence = []
        facts = recall_data.get("results") or recall_data.get("facts") or []
        if isinstance(facts, list):
            for idx, fact in enumerate(facts[:15]):
                if isinstance(fact, dict):
                    text = fact.get("text") or fact.get("content") or fact.get("fact") or str(fact)
                    timestamp = fact.get("timestamp") or fact.get("created_at") or fact.get("date") or "Retained"
                    type_str = fact.get("type") or fact.get("category") or "Memory Fact"
                    evidence.append({
                        "id": fact.get("id") or idx + 1,
                        "text": strip_uuid_citations(text),
                        "timestamp": str(timestamp),
                        "type": str(type_str),
                        "source": "Hindsight Memory Bank"
                    })
                elif isinstance(fact, str):
                    evidence.append({
                        "id": idx + 1,
                        "text": strip_uuid_citations(fact),
                        "timestamp": "Fact",
                        "type": "Fact",
                        "source": "Hindsight Memory Bank"
                    })
        return evidence

    async def generate_meeting_brief(self, deal_id: str) -> Dict[str, Any]:
        """
        1. Query Hindsight recall for comprehensive deal memory
        2. Format normalized recall context
        3. Pass context to LLM with grounded instructions
        """
        deal = get_deal_db(deal_id)
        if not deal:
            raise HTTPException(status_code=404, detail=f"Deal '{deal_id}' not found.")

        deal_name = deal["name"]
        query = (
            f"Prepare for an upcoming sales meeting with {deal_name}. "
            "Retrieve current customer requirements, unresolved objections, "
            "pricing discussions, key stakeholders, competitors, previous commitments, "
            "what changed recently, actions taken, and outcomes of past approaches."
        )

        recall_res = await hindsight_service.recall_deal_memory(deal_id, query, budget="high")
        evidence = self.extract_evidence_from_recall(recall_res)
        normalized_context = self.normalize_recall_context(recall_res)

        system_prompt = (
            load_prompt("meeting_prep.txt") + "\n\n"
            "GROUNDING & FORMATTING RULES:\n"
            "1. Synthesize your executive meeting brief strictly based on the provided Hindsight memory facts.\n"
            "2. Group insights into clear sections: Deal Status, Requirements, Objections, Commercials, Competitors, Outcomes, and Recommended Priorities.\n"
            "3. Do NOT include raw UUIDs, memory IDs, or bracketed ID citations (e.g. 【id】 or (experience id)) in your text.\n"
            "4. Do not invent unbacked customer facts."
        )

        user_prompt = (
            f"DEAL ID: {deal_id}\n"
            f"DEAL NAME: {deal_name}\n"
            f"CLIENT: {deal['client_name']}\n\n"
            f"{normalized_context}\n\n"
            "Generate a grounded Executive Meeting Preparation Brief."
        )

        brief_text = await llm_service.generate_completion(system_prompt, user_prompt)
        clean_brief = strip_uuid_citations(brief_text)

        return {
            "deal_id": deal_id,
            "deal_name": deal_name,
            "meeting_brief": clean_brief,
            "evidence": evidence
        }

    async def ask_deal_agent(self, deal_id: str, question: str) -> Dict[str, Any]:
        """
        1. Query Hindsight for relevant memory facts
        2. Format normalized recall context
        3. Provide direct grounded response
        """
        deal = get_deal_db(deal_id)
        if not deal:
            raise HTTPException(status_code=404, detail=f"Deal '{deal_id}' not found.")

        deal_name = deal["name"]
        recall_res = await hindsight_service.recall_deal_memory(deal_id, question, budget="high")
        evidence = self.extract_evidence_from_recall(recall_res)
        normalized_context = self.normalize_recall_context(recall_res)

        system_prompt = (
            load_prompt("next_action.txt") + "\n\n"
            "GROUNDING & FORMATTING RULES:\n"
            "1. Answer the user's question directly, clearly, and concisely using the provided Hindsight memory facts.\n"
            "2. Cite specific customer facts, stakeholder names, budget figures, or timeline commitments where applicable.\n"
            "3. Do NOT include raw UUIDs, memory IDs, or bracketed citations (such as 【id】 or (experience id)) in the text.\n"
            "4. Do not invent facts not backed by the memory context."
        )

        user_prompt = (
            f"DEAL ID: {deal_id} ({deal_name})\n"
            f"USER QUESTION: {question}\n\n"
            f"{normalized_context}\n\n"
            "Provide a direct, grounded answer citing relevant memory facts where applicable."
        )

        answer_text = await llm_service.generate_completion(system_prompt, user_prompt)
        clean_answer = strip_uuid_citations(answer_text)

        return {
            "deal_id": deal_id,
            "question": question,
            "answer": clean_answer,
            "evidence": evidence
        }

    async def record_interaction_and_learn(
        self,
        deal_id: str,
        type: str,
        date: str,
        title: str,
        transcript: str,
        context: str = "sales meeting"
    ) -> Dict[str, Any]:
        """
        1. Store interaction metadata in SQLite DB
        2. Retain interaction in Hindsight bank with structured type tag
        """
        deal = get_deal_db(deal_id)
        if not deal:
            raise HTTPException(status_code=404, detail=f"Deal '{deal_id}' not found.")

        db_record = add_interaction_db(deal_id, type, date, title, transcript, context)

        formatted_content = (
            f"[{type.upper()}] Date: {date} | Title: {title}\n"
            f"Transcript & Notes:\n{transcript}"
        )

        retain_res = await hindsight_service.retain_memory(
            deal_id=deal_id,
            content=formatted_content,
            context=f"INTERACTION - {type}",
            metadata={"date": date, "title": title, "type": type}
        )

        return {
            "interaction": db_record,
            "hindsight_retention": retain_res
        }

    async def record_outcome_and_learn(
        self,
        deal_id: str,
        action_taken: str,
        result: str,
        impact: str = "positive",
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        1. Store outcome metadata in SQLite database
        2. Retain structured OUTCOME & LEARNING in Hindsight memory bank
        3. Make retrievable for future meeting briefs and strategic decision making
        """
        deal = get_deal_db(deal_id)
        if not deal:
            raise HTTPException(status_code=404, detail=f"Deal '{deal_id}' not found.")

        db_record = add_outcome_db(deal_id, action_taken, result, impact, notes)

        structured_outcome = (
            f"[OUTCOME & LEARNING]\n"
            f"Action Taken by Salesperson: {action_taken}\n"
            f"Customer Result / Response: {result}\n"
            f"Impact Assessment: {impact.upper()}\n"
            f"Strategic Notes: {notes}"
        )

        retain_res = await hindsight_service.retain_memory(
            deal_id=deal_id,
            content=structured_outcome,
            context="OUTCOME - learning and approach result",
            metadata={"type": "outcome", "impact": impact}
        )

        return {
            "outcome": db_record,
            "hindsight_retention": retain_res
        }

deal_agent = DealAgent()
