from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db, list_deals_db, create_or_update_deal_db, add_interaction_db
from backend.api import deals, interactions, agent
from backend.services.hindsight_service import hindsight_service

app = FastAPI(
    title="Deal Intelligence Sales Agent API",
    description="Hindsight Memory Powered Enterprise Sales Intelligence Agent",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

    # Seed default realistic demo deals if DB is empty
    existing_deals = list_deals_db()
    if not existing_deals:
        print("Seeding demo deals...")
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
                print(f"Error initializing Hindsight bank for {d['id']}: {e}")

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": "Deal Intelligence Sales Agent",
        "hindsight_memory": "active"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
