from fastapi import APIRouter, HTTPException
from typing import List
from backend.models.deal import DealCreate
from backend.database import list_deals_db, get_deal_db, create_or_update_deal_db
from backend.services.hindsight_service import hindsight_service

router = APIRouter(prefix="/api/deals", tags=["deals"])

@router.get("", response_model=List[dict])
async def list_deals():
    return list_deals_db()

@router.get("/{deal_id}")
async def get_deal(deal_id: str):
    deal = get_deal_db(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal

@router.post("")
async def create_deal(deal: DealCreate):
    created = create_or_update_deal_db(
        deal_id=deal.id,
        name=deal.name,
        client_name=deal.client_name,
        stage=deal.stage or "Discovery",
        budget=deal.budget or "",
        summary=deal.summary or ""
    )
    # Ensure Hindsight bank exists for this deal
    await hindsight_service.ensure_bank_exists(deal.id, deal.name)
    return created
