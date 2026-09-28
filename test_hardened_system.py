import sys
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import init_db

init_db()
client = TestClient(app)

print("=" * 60)
print("🧪 RUNNING END-TO-END SMOKE TEST WITH ASSERTIONS")
print("=" * 60)

try:
    # 1. Health Endpoint Assertion
    health_res = client.get("/api/health")
    assert health_res.status_code == 200, f"Health check failed: {health_res.text}"
    health_data = health_res.json()
    print("✓ Health Check Passed:", health_data)

    if health_data.get("hindsight") != "healthy" or health_data.get("llm") != "healthy":
        print("\n⚠️ External services (Hindsight or Groq) are not healthy.")
        print("   Hindsight status:", health_data.get("hindsight"))
        print("   LLM status:", health_data.get("llm"))
        print("   External integration tests cannot be fully verified without active credentials.")
        sys.exit(0)

    # 2. Deal Creation Assertion
    deal_res = client.post("/api/deals", json={
        "id": "e2e-acme",
        "name": "E2E Acme Corp",
        "client_name": "E2E Acme Corporation",
        "stage": "Discovery",
        "budget": "₹80,000",
        "summary": "Testing E2E Memory RAG Loop"
    })
    assert deal_res.status_code == 200, f"Deal creation failed: {deal_res.text}"
    print("✓ Deal Creation Passed")

    # 3. First Interaction Creation & Hindsight Retention Assertion
    inter1_res = client.post("/api/deals/e2e-acme/interactions", json={
        "type": "meeting",
        "date": "2026-10-01",
        "title": "Discovery Call",
        "transcript": "Acme needs invoice automation for 10,000 monthly invoices."
    })
    assert inter1_res.status_code == 200, f"Interaction 1 failed: {inter1_res.text}"
    print("✓ First Interaction & Hindsight Retention Passed")

    # 4. Ask Endpoint Assertion
    ask1_res = client.post("/api/deals/e2e-acme/ask", json={
        "question": "What does Acme need?"
    })
    assert ask1_res.status_code == 200, f"Ask 1 failed: {ask1_res.text}"
    assert len(ask1_res.json().get("answer", "")) > 0, "Ask 1 returned empty answer"
    print("✓ First Ask Endpoint Passed")

    # 5. Second Interaction Creation Assertion
    inter2_res = client.post("/api/deals/e2e-acme/interactions", json={
        "type": "meeting",
        "date": "2026-10-05",
        "title": "Objections Review",
        "transcript": "Acme requires deployment within 10 days and considers price of ₹80,000 high."
    })
    assert inter2_res.status_code == 200, f"Interaction 2 failed: {inter2_res.text}"
    print("✓ Second Interaction Passed")

    # 6. Meeting Brief Generation Assertion
    brief_res = client.post("/api/deals/e2e-acme/meeting-brief")
    assert brief_res.status_code == 200, f"Meeting brief failed: {brief_res.text}"
    assert len(brief_res.json().get("meeting_brief", "")) > 0, "Meeting brief returned empty text"
    print("✓ Meeting Brief Generation Passed")

    # 7. Outcome Recording Assertion
    outcome_res = client.post("/api/deals/e2e-acme/outcomes", json={
        "action_taken": "Presented 10-day deployment schedule and proof-of-concept",
        "result": "Client accepted implementation timeline enthusiastically",
        "impact": "positive",
        "notes": "Timeline objection resolved"
    })
    assert outcome_res.status_code == 200, f"Outcome recording failed: {outcome_res.text}"
    print("✓ Outcome Recording Passed")

    # 8. Second Ask Endpoint Assertion
    ask2_res = client.post("/api/deals/e2e-acme/ask", json={
        "question": "What should I prioritize in the next meeting?"
    })
    assert ask2_res.status_code == 200, f"Ask 2 failed: {ask2_res.text}"
    assert len(ask2_res.json().get("answer", "")) > 0, "Ask 2 returned empty answer"
    print("✓ Second Ask Endpoint Passed")

    # 9. Validation & Error Handling Assertions
    err_deal_res = client.get("/api/deals/non-existent-deal/interactions")
    assert err_deal_res.status_code == 404, f"Expected 404, got {err_deal_res.status_code}"
    print("✓ Non-existent Deal 404 Assertion Passed")

    invalid_inter_res = client.post("/api/deals/e2e-acme/interactions", json={
        "type": "meeting",
        "date": "invalid-date-format-xyz",
        "transcript": "This is a sufficiently long transcript for validation."
    })
    assert invalid_inter_res.status_code == 422, f"Expected 422, got {invalid_inter_res.status_code}"
    print("✓ Invalid Interaction Date 422 Assertion Passed")

    print("\n" + "=" * 60)
    print("🎉 ALL END-TO-END ASSERTIONS PASSED SUCCESSFULLY!")
    print("=" * 60)

except AssertionError as assert_err:
    print(f"\n❌ E2E TEST FAILED: {assert_err}")
    sys.exit(1)
except Exception as exc:
    print(f"\n❌ E2E TEST UNEXPECTED ERROR: {exc}")
    sys.exit(1)
