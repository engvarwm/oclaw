import json

from app.core.config import settings
from app.core.errors import OpenClawAdapterError
from app.services.openclaw_client import run_openclaw_agent
from app.services.prompt_renderer import render_prompt
from app.services.response_parser import extract_assistant_text, strip_json_fences


def create_next_step_recommendation(payload: dict) -> dict:
    context_json = json.dumps(payload, ensure_ascii=False, indent=2)
    prompt = render_prompt("deals/next_step.txt", {"context_json": context_json})

    data = run_openclaw_agent(
        session_key=settings.deals_next_step_session_key,
        prompt=prompt,
    )

    answer_text = extract_assistant_text(data)
    if not answer_text:
        answer_text = json.dumps(data, ensure_ascii=False).strip()

    answer_text = strip_json_fences(answer_text)

    try:
        parsed = json.loads(answer_text)
    except json.JSONDecodeError:
        raise OpenClawAdapterError(
            error="invalid_json_from_openclaw",
            message=answer_text[:2000],
        )

    if not isinstance(parsed, dict):
        raise OpenClawAdapterError(
            error="invalid_recommendation_shape",
            message="OpenClaw returned non-object JSON",
        )

    if "recommendation" not in parsed:
        parsed = {
            "ok": True,
            "recommendation": parsed,
        }

    parsed["ok"] = bool(parsed.get("ok", True))
    return parsed
