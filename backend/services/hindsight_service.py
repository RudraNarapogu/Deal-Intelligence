import asyncio
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from hindsight_client import Hindsight
from backend.config import settings

logger = logging.getLogger("deal_intelligence.hindsight")

SALES_RETAIN_MISSION = """
Focus on information relevant to enterprise sales deals:
- Customer requirements and technical specifications
- Unresolved objections, risks, implementation concerns, security worries
- Pricing discussions, budget constraints, commercial terms
- Key stakeholders, decision-makers, internal champions
- Competitors mentioned and comparative pros/cons
- Commitments made by either party and action items
- Actions taken by the salesperson and explicit outcomes
- Strategic learnings from past approaches (what worked, what failed)
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
        self.base_url = settings.HINDSIGHT_BASE_URL

    def _get_client(self) -> Hindsight:
        key = settings.HINDSIGHT_API_KEY.strip()
        if not key:
            raise HTTPException(
                status_code=503,
                detail="Hindsight API key not configured. Long-term deal memory service unavailable."
            )
        return Hindsight(base_url=self.base_url, api_key=key)

    def _get_bank_id(self, deal_id: str) -> str:
        clean_id = str(deal_id).lower().strip().replace(" ", "-").replace("_", "-")
        if not clean_id.startswith("deal-"):
            clean_id = f"deal-{clean_id}"
        return clean_id

    async def check_health(self) -> str:
        client = self._get_client()
        try:
            version = await asyncio.wait_for(client.aget_version(), timeout=5.0)
            if version:
                return "healthy"
            return "unhealthy"
        except Exception as e:
            logger.warning(f"Hindsight Health Check Failed: {str(e)}")
            return "unhealthy"
        finally:
            try:
                await client.aclose()
            except Exception:
                pass

    async def ensure_bank_exists(self, deal_id: str, deal_name: str = "") -> str:
        bank_id = self._get_bank_id(deal_id)
        client = self._get_client()
        try:
            await client.acreate_bank(
                bank_id=bank_id,
                name=deal_name or f"Deal Memory: {deal_id}",
                retain_mission=SALES_RETAIN_MISSION,
                reflect_mission=SALES_REFLECT_MISSION,
                enable_text_search=True,
                enable_temporal_retrieval=True,
                enable_graph_retrieval=True,
                enable_reranking=True
            )
        except Exception as e:
            logger.debug(f"Bank {bank_id} creation response: {e}")
            try:
                await client.aset_mission(bank_id=bank_id, mission=SALES_RETAIN_MISSION)
            except Exception:
                pass
        finally:
            try:
                await client.aclose()
            except Exception:
                pass
        return bank_id

    async def retain_memory(
        self,
        deal_id: str,
        content: str,
        context: str = "sales meeting",
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        bank_id = await self.ensure_bank_exists(deal_id)
        client = self._get_client()
        try:
            response = await client.aretain(
                bank_id=bank_id,
                content=content,
                context=context,
                timestamp=timestamp or datetime.utcnow(),
                metadata=metadata or {}
            )
            return response.to_dict() if hasattr(response, "to_dict") else {"status": "retained", "raw": str(response)}
        except Exception as e:
            logger.error(f"Hindsight retain failed for deal '{deal_id}': {e}")
            raise HTTPException(
                status_code=503,
                detail=f"Hindsight Memory Engine retain operation failed: {str(e)}"
            )
        finally:
            try:
                await client.aclose()
            except Exception:
                pass

    async def recall_deal_memory(
        self,
        deal_id: str,
        query: str,
        budget: str = "high",
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        bank_id = await self.ensure_bank_exists(deal_id)
        client = self._get_client()

        try:
            response = await client.arecall(
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
            logger.error(f"Hindsight recall failed for deal '{deal_id}': {e}")
            raise HTTPException(
                status_code=503,
                detail=f"Hindsight Memory Engine recall operation failed: {str(e)}"
            )
        finally:
            try:
                await client.aclose()
            except Exception:
                pass

    async def reflect_on_deal(
        self,
        deal_id: str,
        query: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        bank_id = await self.ensure_bank_exists(deal_id)
        client = self._get_client()

        try:
            response = await client.areflect(
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
            logger.error(f"Hindsight reflect failed for deal '{deal_id}': {e}")
            raise HTTPException(
                status_code=503,
                detail=f"Hindsight Memory Engine reflect operation failed: {str(e)}"
            )
        finally:
            try:
                await client.aclose()
            except Exception:
                pass

    async def list_deal_memories(
        self,
        deal_id: str,
        limit: int = 50
    ) -> Dict[str, Any]:
        bank_id = await self.ensure_bank_exists(deal_id)
        client = self._get_client()

        try:
            response = await client.alist_memories(
                bank_id=bank_id,
                limit=limit
            )
            if hasattr(response, "model_dump"):
                return response.model_dump()
            elif hasattr(response, "to_dict"):
                return response.to_dict()
            return {"memories": str(response)}
        except Exception as e:
            logger.error(f"Hindsight list_memories failed for deal '{deal_id}': {e}")
            raise HTTPException(
                status_code=503,
                detail=f"Hindsight Memory Engine list_memories operation failed: {str(e)}"
            )
        finally:
            try:
                await client.aclose()
            except Exception:
                pass

hindsight_service = HindsightService()
