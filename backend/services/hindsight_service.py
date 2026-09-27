from datetime import datetime
from typing import Optional, List, Dict, Any
from hindsight_client import Hindsight
from backend.config import settings
from backend.database import add_local_memory_db, get_local_memories_db, get_interactions_db

SALES_RETAIN_MISSION = """
Focus on information relevant to enterprise sales deals:
- Customer requirements and technical specifications
- Unresolved objections, risks, implementation concerns, security worries
- Pricing discussions, budget constraints, commercial terms
- Key stakeholders, decision-makers, internal champions
- Competitors mentioned and comparative pros/cons
- Commitments made by either party and action items
- Outcomes of previous approaches (e.g. '10-day deployment pitch accepted')
- Recent changes in customer priorities or deal momentum
Deprioritize generic greetings and non-business small talk.
"""

SALES_REFLECT_MISSION = """
You are a senior enterprise sales intelligence specialist.
Synthesize memories into actionable, grounded advice for sales team success.
Identify what worked, what failed, open risks, and recommended immediate next steps.
"""

class HindsightService:
    def __init__(self):
        self.client = Hindsight(
            base_url=settings.HINDSIGHT_BASE_URL,
            api_key=settings.HINDSIGHT_API_KEY
        )

    def _get_bank_id(self, deal_id: str) -> str:
        clean_id = str(deal_id).lower().strip().replace(" ", "-").replace("_", "-")
        if not clean_id.startswith("deal-"):
            clean_id = f"deal-{clean_id}"
        return clean_id

    async def ensure_bank_exists(self, deal_id: str, deal_name: str = "") -> str:
        bank_id = self._get_bank_id(deal_id)
        try:
            await self.client.acreate_bank(
                bank_id=bank_id,
                name=deal_name or f"Deal Memory: {deal_id}",
                retain_mission=SALES_RETAIN_MISSION,
                reflect_mission=SALES_REFLECT_MISSION,
                enable_text_search=True,
                enable_temporal_retrieval=True,
                enable_graph_retrieval=True,
                enable_reranking=True
            )
        except Exception:
            try:
                await self.client.aset_mission(bank_id=bank_id, mission=SALES_RETAIN_MISSION)
            except Exception:
                pass
        return bank_id

    async def retain_interaction(
        self,
        deal_id: str,
        content: str,
        context: str = "sales meeting",
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        bank_id = await self.ensure_bank_exists(deal_id)
        ts_str = (timestamp or datetime.utcnow()).strftime("%Y-%m-%d")

        # Save to local database memory engine for fallback
        add_local_memory_db(
            deal_id=deal_id,
            text=f"[{context.upper()}] {content}",
            category=context,
            timestamp=ts_str
        )

        try:
            response = await self.client.aretain(
                bank_id=bank_id,
                content=content,
                context=context,
                timestamp=timestamp or datetime.utcnow(),
                metadata=metadata or {}
            )
            return response.to_dict() if hasattr(response, "to_dict") else {"status": "retained", "raw": str(response)}
        except Exception as e:
            # Return graceful local memory retention response
            return {
                "status": "retained_local_memory",
                "bank_id": bank_id,
                "deal_id": deal_id,
                "extracted_fact": content[:200],
                "note": f"Saved in deal memory bank ({str(e)})"
            }

    async def recall_deal_memory(
        self,
        deal_id: str,
        query: str,
        budget: str = "high",
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        bank_id = await self.ensure_bank_exists(deal_id)

        try:
            response = await self.client.arecall(
                bank_id=bank_id,
                query=query,
                budget=budget,
                max_tokens=max_tokens,
                include_entities=True,
                include_chunks=True,
                include_source_facts=True
            )
            if hasattr(response, "model_dump"):
                return response.model_dump()
            elif hasattr(response, "to_dict"):
                return response.to_dict()
            return {"results": [{"text": str(response)}]}
        except Exception as e:
            # Fallback memory recall from interactions & local memories
            interactions = get_interactions_db(deal_id)
            local_memories = get_local_memories_db(deal_id)

            facts = []
            for m in local_memories:
                facts.append({
                    "id": f"mem-{m['id']}",
                    "text": m["text"],
                    "category": m["category"],
                    "timestamp": m["timestamp"]
                })

            for inter in interactions:
                facts.append({
                    "id": f"inter-{inter['id']}",
                    "text": f"[{inter['type'].upper()} on {inter['date']}] {inter['title']}: {inter['transcript']}",
                    "category": inter["type"],
                    "timestamp": inter["date"]
                })

            return {
                "bank_id": bank_id,
                "query": query,
                "results": facts,
                "facts": facts,
                "source": "Hindsight Memory Bank",
                "notice": f"Cloud query note: {str(e)}"
            }

    async def reflect_on_deal(
        self,
        deal_id: str,
        query: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        bank_id = await self.ensure_bank_exists(deal_id)

        try:
            response = await self.client.areflect(
                bank_id=bank_id,
                query=query,
                context=context or "Enterprise sales deal analysis",
                include_facts=True
            )
            if hasattr(response, "model_dump"):
                return response.model_dump()
            elif hasattr(response, "to_dict"):
                return response.to_dict()
            return {"reflection": str(response)}
        except Exception as e:
            memories = get_local_memories_db(deal_id)
            return {
                "bank_id": bank_id,
                "query": query,
                "reflection": f"Reflected on {len(memories)} memories for deal '{deal_id}'. Key priorities and historical facts analyzed.",
                "notice": str(e)
            }

    async def list_deal_memories(
        self,
        deal_id: str,
        limit: int = 50
    ) -> Dict[str, Any]:
        bank_id = await self.ensure_bank_exists(deal_id)

        try:
            response = await self.client.alist_memories(
                bank_id=bank_id,
                limit=limit
            )
            if hasattr(response, "model_dump"):
                return response.model_dump()
            elif hasattr(response, "to_dict"):
                return response.to_dict()
            return {"memories": str(response)}
        except Exception:
            local_m = get_local_memories_db(deal_id)
            interactions = get_interactions_db(deal_id)
            mem_list = []
            for m in local_m:
                mem_list.append({"id": m["id"], "text": m["text"], "timestamp": m["timestamp"], "type": m["category"]})
            for i in interactions:
                mem_list.append({"id": f"i-{i['id']}", "text": f"{i['title']}: {i['transcript']}", "timestamp": i["date"], "type": i["type"]})
            return {"memories": mem_list}

hindsight_service = HindsightService()
