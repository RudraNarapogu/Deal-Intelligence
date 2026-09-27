from fastapi import APIRouter, HTTPException
from backend.models.interaction import AskAgentRequest, ReflectRequest
from backend.database import get_deal_db
from backend.services.deal_agent import deal_agent
from backend.services.hindsight_service import hindsight_service

router = APIRouter(prefix="/api/deals/{deal_id}", tags=["agent"])

@router.post("/meeting-brief")
async def get_meeting_brief(deal_id: str):
    deal = get_deal_db(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    brief = await deal_agent.generate_meeting_brief(deal_id)
    return brief

@router.post("/ask")
async def ask_agent(deal_id: str, payload: AskAgentRequest):
    deal = get_deal_db(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    response = await deal_agent.ask_deal_agent(deal_id, payload.question)
    return response

@router.get("/memories")
async def get_memories(deal_id: str, limit: int = 50):
    deal = get_deal_db(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    memories = await hindsight_service.list_deal_memories(deal_id, limit=limit)
    return memories

@router.post("/reflect")
async def reflect_agent(deal_id: str, payload: ReflectRequest):
    deal = get_deal_db(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    reflect_res = await hindsight_service.reflect_on_deal(
        deal_id=deal_id,
        query=payload.query,
        context=payload.context
    )
    return reflect_res
