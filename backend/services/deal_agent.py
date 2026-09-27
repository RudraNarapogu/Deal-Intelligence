import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from backend.services.hindsight_service import hindsight_service
from backend.services.llm_service import llm_service
from backend.database import get_deal_db, get_interactions_db, add_interaction_db

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

def load_prompt(filename: str) -> str:
    path = PROMPTS_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "You are a helpful sales deal intelligence agent."

class DealAgent:
    def extract_evidence_from_recall(self, recall_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract clean, human-readable memory evidence items from Hindsight recall response
        to display to judges in the UI timeline & evidence section.
        """
        evidence = []

        # Check for results or facts in recall response
        facts = recall_data.get("results", []) or recall_data.get("facts", []) or []
        if isinstance(facts, list):
            for idx, fact in enumerate(facts[:15]):
                if isinstance(fact, dict):
                    text = fact.get("text") or fact.get("content") or fact.get("fact") or str(fact)
                    timestamp = fact.get("timestamp") or fact.get("created_at") or fact.get("date") or "Retrieved Memory"
                    type_str = fact.get("type") or fact.get("category") or "Memory Fact"
                    evidence.append({
                        "id": idx + 1,
                        "text": text,
                        "timestamp": str(timestamp),
                        "type": str(type_str)
                    })
                elif isinstance(fact, str):
                    evidence.append({
                        "id": idx + 1,
                        "text": fact,
                        "timestamp": "Historical Fact",
                        "type": "Fact"
                    })

        # Fallback if raw or direct structure
        if not evidence and "raw" in recall_data:
            evidence.append({
                "id": 1,
                "text": str(recall_data["raw"])[:300],
                "timestamp": "Hindsight Recall",
                "type": "Memory"
            })

        return evidence

    async def generate_meeting_brief(self, deal_id: str) -> Dict[str, Any]:
        """
        1. Query Hindsight recall for comprehensive deal memory
        2. Pass context to LLM for meeting preparation brief
        3. Extract memory evidence sources for transparency
        """
        deal = get_deal_db(deal_id)
        deal_name = deal.get("name") if deal else deal_id

        query = (
            f"Prepare for an upcoming sales meeting with {deal_name}. "
            "Retrieve current customer requirements, unresolved objections, "
            "pricing discussions, key stakeholders, competitors, previous commitments, "
            "what changed recently, and previous successful or unsuccessful sales approaches."
        )

        # 1. Recall memories from Hindsight
        recall_res = await hindsight_service.recall_deal_memory(deal_id, query, budget="high")
        evidence = self.extract_evidence_from_recall(recall_res)

        # Prepare context for LLM
        system_prompt = load_prompt("meeting_prep.txt")
        context_str = json.dumps(recall_res, indent=2, default=str)

        user_prompt = (
            f"DEAL ID: {deal_id}\n"
            f"DEAL NAME: {deal_name}\n\n"
            f"RETRIVED HINDSIGHT MEMORY CONTEXT:\n{context_str}\n\n"
            "Generate a structured, actionable Meeting Brief."
        )

        # 2. LLM synthesis
        brief_text = await llm_service.generate_completion(system_prompt, user_prompt)

        return {
            "deal_id": deal_id,
            "deal_name": deal_name,
            "meeting_brief": brief_text,
            "evidence": evidence,
            "raw_recall": recall_res
        }

    async def ask_deal_agent(self, deal_id: str, question: str) -> Dict[str, Any]:
        """
        1. Query Hindsight for relevant memory context to answer user question
        2. Format answer using LLM
        3. Return grounded answer + memory evidence
        """
        deal = get_deal_db(deal_id)
        deal_name = deal.get("name") if deal else deal_id

        # Query Hindsight recall
        recall_res = await hindsight_service.recall_deal_memory(deal_id, question, budget="high")
        evidence = self.extract_evidence_from_recall(recall_res)

        system_prompt = load_prompt("next_action.txt")
        context_str = json.dumps(recall_res, indent=2, default=str)

        user_prompt = (
            f"DEAL ID: {deal_id} ({deal_name})\n"
            f"USER QUESTION: {question}\n\n"
            f"HINDSIGHT MEMORY EVIDENCE:\n{context_str}\n\n"
            "Provide a direct, grounded answer with clear action recommendations."
        )

        answer = await llm_service.generate_completion(system_prompt, user_prompt)

        return {
            "deal_id": deal_id,
            "question": question,
            "answer": answer,
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
        1. Save interaction to SQLite DB
        2. Retain interaction in Hindsight bank
        """
        db_record = add_interaction_db(deal_id, type, date, title, transcript, context)

        full_content = f"Date: {date}\nTitle: {title}\nType: {type}\n\nTranscript / Content:\n{transcript}"

        retain_res = await hindsight_service.retain_interaction(
            deal_id=deal_id,
            content=full_content,
            context=f"{type} - {context}",
            metadata={"date": date, "title": title, "type": type}
        )

        return {
            "interaction": db_record,
            "hindsight_retention": retain_res
        }

deal_agent = DealAgent()
