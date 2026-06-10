from pathlib import Path


class SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return "unknown"


_PROMPTS_ROOT = Path(__file__).resolve().parent.parent / "prompts"


def render_prompt(template_path: str, context: dict) -> str:
    path = _PROMPTS_ROOT / template_path
    template = path.read_text(encoding="utf-8")
    safe_context = SafeDict({key: ("" if value is None else value) for key, value in context.items()})
    return template.format_map(safe_context).strip()
