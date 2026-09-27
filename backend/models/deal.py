from pydantic import BaseModel, Field
from typing import Optional

class DealCreate(BaseModel):
    id: str = Field(..., min_length=2, description="Unique deal identifier")
    name: str = Field(..., min_length=2, description="Deal name")
    client_name: str = Field(..., min_length=2, description="Client organization name")
    stage: Optional[str] = Field("Discovery", description="Sales pipeline stage")
    budget: Optional[str] = Field("", description="Target value or budget")
    summary: Optional[str] = Field("", description="Deal summary objective")

class DealResponse(BaseModel):
    id: str
    name: str
    client_name: str
    stage: str
    budget: str
    summary: str
    created_at: str
    updated_at: str
