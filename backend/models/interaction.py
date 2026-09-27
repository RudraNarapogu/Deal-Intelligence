from pydantic import BaseModel, Field
from typing import Optional

class InteractionCreate(BaseModel):
    type: str = Field(..., min_length=1, description="Type of interaction (meeting, email, call, note)")
    date: str = Field(..., min_length=5, description="Date in YYYY-MM-DD format")
    title: Optional[str] = Field("", description="Title or topic")
    transcript: str = Field(..., min_length=1, description="Full transcript or interaction text")
    context: Optional[str] = Field("sales meeting", description="Sales context")

class OutcomeCreate(BaseModel):
    action_taken: str = Field(..., min_length=1, description="Sales approach or action taken")
    result: str = Field(..., min_length=1, description="Client response or result")
    impact: str = Field("positive", description="Impact rating: positive, negative, or neutral")
    notes: Optional[str] = Field("", description="Additional strategic notes or learnings")

class AskAgentRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question about the deal")

class ReflectRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Strategic reflection query")
    context: Optional[str] = Field("Sales Deal Strategic Analysis", description="Reflection context")
