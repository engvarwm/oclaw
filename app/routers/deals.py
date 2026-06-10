from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from app.core.errors import OpenClawAdapterError
from app.core.security import verify_hub_token
from app.schemas.deals import DealsDraftReplyRequest, DealsNextStepRequest
from app.services.deals.draft_reply_service import create_draft_reply
from app.services.deals.next_step_service import create_next_step_recommendation

router = APIRouter(tags=["deals"])


@router.post("/draft-reply")
async def draft_reply(
    payload: DealsDraftReplyRequest,
    authorization: str | None = Header(default=None),
):
    verify_hub_token(authorization)

    try:
        draft = create_draft_reply(payload.model_dump())
    except OpenClawAdapterError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "ok": False,
                "error": exc.error,
                "message": exc.message,
            },
        )

    return {"ok": True, "draft_reply": draft}


@router.post("/next-step")
async def recommend_next_step(
    payload: DealsNextStepRequest,
    authorization: str | None = Header(default=None),
):
    verify_hub_token(authorization)

    try:
        result = create_next_step_recommendation(payload.model_dump())
    except OpenClawAdapterError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "ok": False,
                "error": exc.error,
                "message": exc.message,
            },
        )

    return result
