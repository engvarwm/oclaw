import json


def test_next_step_without_token_returns_401(client):
    response = client.post("/deals/next-step", json={"deal": {"id": 1}})
    assert response.status_code == 401


def test_next_step_with_wrong_token_returns_401(client):
    response = client.post(
        "/deals/next-step",
        json={"deal": {"id": 1}},
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert response.status_code == 401


def test_next_step_success_with_recommendation_wrapper(client, auth_headers, monkeypatch):
    recommendation = {
        "decision": "adapt_next_step",
        "base_scenario": "standard",
        "recommended_step": {
            "title": "Follow-up email",
            "type": "email",
            "description": "Отправить уточняющее письмо",
            "due_in_hours": 24,
        },
    }

    def fake_run_openclaw_agent(**_kwargs):
        return {
            "result": {
                "payloads": [{"text": json.dumps({"recommendation": recommendation})}],
            }
        }

    monkeypatch.setattr(
        "app.services.deals.next_step_service.run_openclaw_agent",
        fake_run_openclaw_agent,
    )

    response = client.post(
        "/deals/next-step",
        json={"deal": {"id": 1}, "timeline": [], "messages": []},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["recommendation"]["decision"] == "adapt_next_step"


def test_next_step_wraps_flat_json(client, auth_headers, monkeypatch):
    flat = {
        "decision": "keep_next_step",
        "base_scenario": "fast",
        "recommended_step": {
            "title": "Call client",
            "type": "call",
            "description": "Позвонить клиенту",
            "due_in_hours": 4,
        },
    }

    def fake_run_openclaw_agent(**_kwargs):
        return {"result": {"finalAssistantVisibleText": json.dumps(flat)}}

    monkeypatch.setattr(
        "app.services.deals.next_step_service.run_openclaw_agent",
        fake_run_openclaw_agent,
    )

    response = client.post(
        "/deals/next-step",
        json={"deal": {"id": 2}},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["recommendation"]["decision"] == "keep_next_step"


def test_next_step_strips_markdown_fences(client, auth_headers, monkeypatch):
    payload = {
        "ok": True,
        "recommendation": {
            "decision": "insert_step",
            "base_scenario": "strategic",
            "recommended_step": {
                "title": "Meeting",
                "type": "meeting",
                "description": "Назначить встречу",
                "due_in_hours": 48,
            },
        },
    }

    fenced = f"```json\n{json.dumps(payload)}\n```"

    def fake_run_openclaw_agent(**_kwargs):
        return {"result": {"payloads": [{"text": fenced}]}}

    monkeypatch.setattr(
        "app.services.deals.next_step_service.run_openclaw_agent",
        fake_run_openclaw_agent,
    )

    response = client.post(
        "/deals/next-step",
        json={"deal": {"id": 3}},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["recommendation"]["decision"] == "insert_step"
