from fastapi import HTTPException

from app.core.config import settings


def verify_hub_token(authorization: str | None) -> None:
    if not settings.hub_openclaw_token:
        raise HTTPException(
            status_code=500,
            detail="HUB_OPENCLAW_TOKEN is not configured",
        )

    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    expected = f"Bearer {settings.hub_openclaw_token}"
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")
