import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import init_db, list_deals_db, create_or_update_deal_db
from backend.api import deals, interactions, agent
from backend.services.hindsight_service import hindsight_service
from backend.services.llm_service import llm_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("deal_intelligence")

app = FastAPI(
    title="Deal Intelligence Sales Agent API",
    description="Hindsight Memory Powered Enterprise Sales Intelligence Agent",
    version="1.0.0"
)

# Configure explicit CORS origins
allowed_origins = [
    settings.FRONTEND_URL.rstrip("/"),
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deals.router)
app.include_router(interactions.router)
app.include_router(agent.router)

@app.on_event("startup")
async def startup_event():
    init_db()

    existing_deals = list_deals_db()
    if not existing_deals:
        logger.info("Seeding initial demo deals...")
        demo_deals = [
            {
                "id": "acme-corp",
                "name": "Acme Corp",
                "client_name": "Acme Corporation",
                "stage": "Evaluation",
                "budget": "₹80,000",
                "summary": "Enterprise invoice automation & cloud integration"
            },
            {
                "id": "zenith-ltd",
                "name": "Zenith Ltd",
                "client_name": "Zenith Logistics",
                "stage": "Negotiation",
                "budget": "₹150,000",
                "summary": "Fleet management workflow modernization"
            },
            {
                "id": "nova-systems",
                "name": "Nova Systems",
                "client_name": "Nova Health Systems",
                "stage": "Discovery",
                "budget": "₹50,000",
                "summary": "Patient intake record digitization"
            }
        ]
        for d in demo_deals:
            create_or_update_deal_db(
                deal_id=d["id"],
                name=d["name"],
                client_name=d["client_name"],
                stage=d["stage"],
                budget=d["budget"],
                summary=d["summary"]
            )
            try:
                await hindsight_service.ensure_bank_exists(d["id"], d["name"])
            except Exception as e:
                logger.warning(f"Note on Hindsight bank setup for {d['id']}: {e}")

@app.get("/api/health")
async def health_check():
    """
    Real health check endpoint inspecting status of API, Hindsight, and LLM provider.
    """
    hindsight_status = await hindsight_service.check_health()
    llm_status = await llm_service.check_health()

    return {
        "api": "healthy",
        "hindsight": hindsight_status,
        "llm": llm_status
    }

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": "Deal Intelligence Sales Agent",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
