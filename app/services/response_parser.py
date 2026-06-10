import json


def extract_assistant_text(result: dict) -> str:
    text = ""

    if isinstance(result, dict):
        result_obj = result.get("result") or {}

        if isinstance(result_obj, dict):
            payloads = result_obj.get("payloads") or []

            if isinstance(payloads, list) and payloads:
                first_payload = payloads[0] or {}
                if isinstance(first_payload, dict):
                    text = first_payload.get("text") or ""

            if not text:
                text = (
                    result_obj.get("finalAssistantVisibleText")
                    or result_obj.get("finalAssistantRawText")
                    or ""
                )

        if not text:
            text = (
                result.get("finalAssistantVisibleText")
                or result.get("finalAssistantRawText")
                or result.get("reply")
                or result.get("message")
                or result.get("text")
                or result.get("content")
                or ""
            )

    if isinstance(text, dict):
        text = json.dumps(text, ensure_ascii=False)

    return str(text).strip()


def strip_json_fences(text: str) -> str:
    cleaned = text.strip()
    if not cleaned.startswith("```"):
        return cleaned

    cleaned = cleaned.strip("`").strip()
    if cleaned.startswith("json"):
        cleaned = cleaned[4:].strip()
    return cleaned
