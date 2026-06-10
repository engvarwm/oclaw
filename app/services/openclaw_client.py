import json
import logging
import subprocess

from app.core.config import settings
from app.core.errors import BadOpenClawResponseError, OpenClawUnavailableError

logger = logging.getLogger(__name__)


def run_openclaw_agent(
    *,
    session_key: str,
    prompt: str,
    timeout: int | None = None,
) -> dict:
    openclaw_timeout = timeout or settings.openclaw_timeout_seconds
    cmd = [
        settings.openclaw_bin,
        "agent",
        "--session-key",
        session_key,
        "--message",
        prompt,
        "--json",
        "--timeout",
        str(openclaw_timeout),
    ]

    try:
        result = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            timeout=settings.openclaw_subprocess_timeout_seconds,
        )
    except Exception as exc:
        logger.error("OpenClaw subprocess failed: %s", type(exc).__name__)
        raise OpenClawUnavailableError(
            message=str(exc),
            error="openclaw_exec_error",
        ) from exc

    if result.returncode != 0:
        stderr_tail = (result.stderr or "")[-1000:]
        logger.error(
            "OpenClaw exited with code %s: %s",
            result.returncode,
            stderr_tail[:200],
        )
        raise OpenClawUnavailableError(
            message=stderr_tail,
            error="openclaw_failed",
        )

    raw = (result.stdout or "").strip()
    if not raw:
        raise BadOpenClawResponseError(
            message="OpenClaw returned empty stdout",
            error="empty_openclaw_response",
        )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("OpenClaw JSON parse failed: %s", type(exc).__name__)
        raise BadOpenClawResponseError(
            message="Failed to parse OpenClaw JSON response",
            error="invalid_openclaw_json",
        ) from exc

    if not isinstance(data, dict):
        raise BadOpenClawResponseError(
            message="OpenClaw returned non-object JSON",
            error="invalid_openclaw_json",
        )

    return data
