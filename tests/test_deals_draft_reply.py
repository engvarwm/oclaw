def test_draft_reply_without_token_returns_401(client):
    response = client.post(
        "/deals/draft-reply",
        json={"message": {"subject": "Hi", "body": "Hello"}},
    )
    assert response.status_code == 401


def test_draft_reply_with_wrong_token_returns_401(client):
    response = client.post(
        "/deals/draft-reply",
        json={"message": {"subject": "Hi", "body": "Hello"}},
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert response.status_code == 401


def test_draft_reply_empty_body(client, auth_headers):
    response = client.post(
        "/deals/draft-reply",
        json={"message": {"subject": "Hi", "body": "   "}},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is False
    assert data["error"] == "empty_body"


def test_draft_reply_success(client, auth_headers, monkeypatch):
    def fake_run_openclaw_agent(**_kwargs):
        return {
            "result": {
                "payloads": [{"text": "Спасибо за письмо. Уточните, пожалуйста, объём заказа."}],
            }
        }

    monkeypatch.setattr(
        "app.services.deals.draft_reply_service.run_openclaw_agent",
        fake_run_openclaw_agent,
    )

    response = client.post(
        "/deals/draft-reply",
        json={"message": {"subject": "Запрос", "body": "Нужна цена на оборудование."}},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["draft_reply"] == "Спасибо за письмо. Уточните, пожалуйста, объём заказа."


def test_draft_reply_supports_flat_payload_fields(client, auth_headers, monkeypatch):
    def fake_run_openclaw_agent(**_kwargs):
        return {"result": {"finalAssistantVisibleText": "Черновик ответа"}}

    monkeypatch.setattr(
        "app.services.deals.draft_reply_service.run_openclaw_agent",
        fake_run_openclaw_agent,
    )

    response = client.post(
        "/deals/draft-reply",
        json={
            "subject": "Тема",
            "body": "Текст письма",
            "deal_scenario": "standard",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["draft_reply"] == "Черновик ответа"
