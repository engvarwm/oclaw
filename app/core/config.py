import os

from pydantic import BaseModel


class Settings(BaseModel):
    hub_openclaw_token: str = os.getenv("HUB_OPENCLAW_TOKEN", "")
    openclaw_bin: str = os.getenv("OPENCLAW_BIN", "openclaw")
    openclaw_timeout_seconds: int = int(os.getenv("OPENCLAW_TIMEOUT_SECONDS", "180"))
    openclaw_subprocess_timeout_seconds: int = int(
        os.getenv("OPENCLAW_SUBPROCESS_TIMEOUT_SECONDS", "190")
    )
    service_name: str = os.getenv("HUB_SERVICE_NAME", "hub-openclaw-adapter")

    deals_draft_session_key: str = os.getenv(
        "HUB_DEALS_DRAFT_SESSION_KEY", "agent:hub:deals-draft"
    )
    deals_next_step_session_key: str = os.getenv(
        "HUB_DEALS_NEXT_STEP_SESSION_KEY", "agent:hub:deals-next-step"
    )


settings = Settings()
