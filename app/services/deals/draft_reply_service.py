import json

from app.core.config import settings
from app.core.errors import OpenClawAdapterError
from app.services.openclaw_client import run_openclaw_agent
from app.services.prompt_renderer import render_prompt
from app.services.response_parser import extract_assistant_text


def _format_context_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)


def normalize_draft_reply_context(payload: dict) -> dict:
    message = payload.get("message") or {}

    subject = payload.get("subject")
    if subject is None:
        subject = message.get("subject") if isinstance(message, dict) else ""

    body = payload.get("body")
    if body is None:
        body = message.get("body") if isinstance(message, dict) else ""

    return {
        "subject": subject or "",
        "body": body or "",
        "deal_scenario": _format_context_value(payload.get("deal_scenario")),
        "deal_stage": _format_context_value(payload.get("deal_stage")),
        "deal_status": _format_context_value(payload.get("deal_status")),
        "deal_amount": _format_context_value(payload.get("deal_amount")),
        "current_touch_step": _format_context_value(payload.get("current_touch_step")),
        "recent_timeline": _format_context_value(payload.get("recent_timeline")),
        "recent_messages": _format_context_value(payload.get("recent_messages")),
        "sender_profile": _format_context_value(payload.get("sender_profile")),
        "attachments_summary": _format_context_value(payload.get("attachments_summary")),
    }


def create_draft_reply(payload: dict) -> str:
    context = normalize_draft_reply_context(payload)

    if not context["body"].strip():
        raise OpenClawAdapterError(
            error="empty_body",
            message="Empty message body",
        )

    prompt = render_prompt("deals/draft_reply.txt", context)

    data = run_openclaw_agent(
        session_key=settings.deals_draft_session_key,
        prompt=prompt,
    )

    draft = extract_assistant_text(data)
    if not draft:
        draft = json.dumps(data, ensure_ascii=False).strip()

    if not draft:
        raise OpenClawAdapterError(
            error="empty_draft",
            message="OpenClaw returned empty draft",
        )

    return draft
