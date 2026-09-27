import asyncio
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import init_db

init_db()
client = TestClient(app)

print("=" * 60)
print("🧪 STARTING MANDATORY END-TO-END TESTING")
print("=" * 60)

# STEP 1: Health Check
print("\n--- TEST 1: Health Check ---")
health_res = client.get("/api/health")
print("Health Check HTTP Status:", health_res.status_code)
print("Health Check Body:", health_res.json())

# STEP 2: Create Test Deal
print("\n--- TEST 2: Create Deal 'test-acme' ---")
create_res = client.post("/api/deals", json={
    "id": "test-acme",
    "name": "Test Acme Corp",
    "client_name": "Acme Corporation Test",
    "stage": "Discovery",
    "budget": "₹80,000",
    "summary": "Testing Hindsight RAG loop"
})
print("Create Deal HTTP Status:", create_res.status_code)

# STEP 3: Add First Interaction
print("\n--- TEST 3: Add Interaction 1 (Invoice Automation) ---")
inter1_res = client.post("/api/deals/test-acme/interactions", json={
    "type": "meeting",
    "date": "2026-10-01",
    "title": "Discovery Meeting",
    "transcript": "Acme needs invoice automation to process 10,000 invoices monthly."
})
print("Interaction 1 HTTP Status:", inter1_res.status_code)
print("Retain Response:", inter1_res.json().get("hindsight_retention"))

# STEP 4: Query Hindsight Recall
print("\n--- TEST 4: Query 'What does Acme need?' ---")
ask1_res = client.post("/api/deals/test-acme/ask", json={
    "question": "What does Acme need?"
})
print("Ask 1 HTTP Status:", ask1_res.status_code)
print("Ask 1 Answer Snippet:", ask1_res.json().get("answer", "")[:300])

# STEP 5: Add Second Interaction
print("\n--- TEST 5: Add Interaction 2 (Timeline & Price Objection) ---")
inter2_res = client.post("/api/deals/test-acme/interactions", json={
    "type": "meeting",
    "date": "2026-10-05",
    "title": "Requirements & Objections",
    "transcript": "Acme requires deployment within 10 days and considers our price of ₹80,000 high."
})
print("Interaction 2 HTTP Status:", inter2_res.status_code)

# STEP 6: Generate Meeting Brief
print("\n--- TEST 6: Prepare Meeting Brief (Must combine Interaction 1 & 2) ---")
brief_res = client.post("/api/deals/test-acme/meeting-brief")
print("Brief HTTP Status:", brief_res.status_code)
brief_text = brief_res.json().get("meeting_brief", "")
print("Brief Text Snippet:", brief_text[:400])

# STEP 7: Record Outcome & Learning
print("\n--- TEST 7: Record Explicit Outcome ---")
outcome_res = client.post("/api/deals/test-acme/outcomes", json={
    "action_taken": "Presented a 10-day implementation plan and ROI breakdown",
    "result": "Client accepted the implementation timeline enthusiastically",
    "impact": "positive",
    "notes": "Timeline fear resolved. Pricing accepted."
})
print("Outcome HTTP Status:", outcome_res.status_code)

# STEP 8: Ask Strategic Recommendation (Must use Outcome)
print("\n--- TEST 8: Strategic Priority Query (Using Past Outcome) ---")
ask2_res = client.post("/api/deals/test-acme/ask", json={
    "question": "What should I prioritize in the next Acme meeting?"
})
print("Ask 2 HTTP Status:", ask2_res.status_code)
print("Ask 2 Answer Snippet:", ask2_res.json().get("answer", "")[:400])

# FAILURE TESTING
print("\n--- TEST 9: Failure Testing (Unknown Deal & Invalid Requests) ---")
err_deal = client.get("/api/deals/non-existent-deal/interactions")
print("Non-existent Deal HTTP Status:", err_deal.status_code)

invalid_inter = client.post("/api/deals/test-acme/interactions", json={
    "type": "",
    "date": "",
    "transcript": "a"
})
print("Invalid Interaction HTTP Status:", invalid_inter.status_code)

print("\n" + "=" * 60)
print("✅ END-TO-END MANDATORY TESTS COMPLETED")
print("=" * 60)
