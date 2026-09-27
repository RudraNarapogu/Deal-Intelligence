import asyncio
import logging
from backend.services.deal_agent import deal_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed_memories")

async def seed_all_deal_memories():
    logger.info("Seeding realistic deal memories into Hindsight Memory Banks...")

    # 1. ACME CORP
    acme_history = [
        {
            "type": "meeting",
            "date": "2026-09-05",
            "title": "Initial Discovery Meeting",
            "transcript": "Met with Sarah Jenkins (VP Finance, Acme Corp). Acme processes 10,000 invoices monthly manually and requires an automated invoice processing solution. Approved budget: ₹80,000."
        },
        {
            "type": "meeting",
            "date": "2026-09-12",
            "title": "Requirements & Competitor Review",
            "transcript": "Sarah Jenkins emphasized that implementation MUST be completed within 10 days due to upcoming Q4 financial reporting. Competitor X offered ₹70,000 but lacks automated reconciliation and cloud security compliance."
        },
        {
            "type": "meeting",
            "date": "2026-09-18",
            "title": "Security & Compliance Review",
            "transcript": "David Vance (CSO) joined. Major security objection raised regarding multi-tenant data storage and SOC2 compliance. Pricing of ₹80,000 was approved by Sarah pending security clearance."
        }
    ]

    for item in acme_history:
        await deal_agent.record_interaction_and_learn(
            deal_id="acme-corp",
            type=item["type"],
            date=item["date"],
            title=item["title"],
            transcript=item["transcript"]
        )

    await deal_agent.record_outcome_and_learn(
        deal_id="acme-corp",
        action_taken="Presented a 10-day deployment schedule and proof-of-concept plan to Sarah Jenkins",
        result="Client accepted the 10-day implementation timeline enthusiastically",
        impact="positive",
        notes="Implementation concern resolved. David Vance requested SOC2 security architecture whitepaper."
    )

    # 2. ZENITH LTD
    zenith_history = [
        {
            "type": "meeting",
            "date": "2026-09-10",
            "title": "Fleet Management Discovery",
            "transcript": "Met with Marcus Vance (Operations Director, Zenith Ltd). Managing 500 delivery vehicles manually. Needs real-time GPS telematics and driver mobile app. Budget: ₹150,000."
        },
        {
            "type": "meeting",
            "date": "2026-09-15",
            "title": "Offline Sync & Driver Adoption",
            "transcript": "Marcus raised concerns regarding driver adoption and mobile app offline sync in rural delivery zones."
        }
    ]

    for item in zenith_history:
        await deal_agent.record_interaction_and_learn(
            deal_id="zenith-ltd",
            type=item["type"],
            date=item["date"],
            title=item["title"],
            transcript=item["transcript"]
        )

    await deal_agent.record_outcome_and_learn(
        deal_id="zenith-ltd",
        action_taken="Conducted live offline-first mobile app demo showing instant sync",
        result="Marcus accepted driver adoption strategy and validated offline sync capabilities",
        impact="positive",
        notes="Offline sync concern resolved. Moving to contract negotiation."
    )

    # 3. NOVA SYSTEMS
    nova_history = [
        {
            "type": "meeting",
            "date": "2026-09-08",
            "title": "Patient Intake Digitization",
            "transcript": "Met with Dr. Aris Thorne (CIO, Nova Health Systems). Goal: Digitize patient intake records across 12 clinics. Budget: ₹50,000. Requirement: HIPAA compliance certification and EHR system integration."
        }
    ]

    for item in nova_history:
        await deal_agent.record_interaction_and_learn(
            deal_id="nova-systems",
            type=item["type"],
            date=item["date"],
            title=item["title"],
            transcript=item["transcript"]
        )

    logger.info("Successfully seeded all deal memories into Hindsight Memory Engine!")

if __name__ == "__main__":
    asyncio.run(seed_all_deal_memories())
