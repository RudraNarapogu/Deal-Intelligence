from fastapi import APIRouter, HTTPException
from backend.models.interaction import InteractionCreate
from backend.database import get_deal_db, get_interactions_db
from backend.services.deal_agent import deal_agent

router = APIRouter(prefix="/api/deals/{deal_id}/interactions", tags=["interactions"])

@router.get("")
async def list_interactions(deal_id: str):
    deal = get_deal_db(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return get_interactions_db(deal_id)

@router.post("")
async def create_interaction(deal_id: str, payload: InteractionCreate):
    deal = get_deal_db(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    result = await deal_agent.record_interaction_and_learn(
        deal_id=deal_id,
        type=payload.type,
        date=payload.date,
        title=payload.title or f"{payload.type.capitalize()} on {payload.date}",
        transcript=payload.transcript,
        context=payload.context or "sales meeting"
    )
    return result
