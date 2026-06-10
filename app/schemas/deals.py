from typing import Any

from pydantic import BaseModel, ConfigDict


class DealsDraftReplyRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    subject: str | None = None
    body: str | None = None
    deal_scenario: str | None = None
    deal_stage: str | None = None
    deal_status: str | None = None
    deal_amount: Any | None = None
    current_touch_step: Any | None = None
    recent_timeline: Any | None = None
    recent_messages: Any | None = None
    sender_profile: Any | None = None
    attachments_summary: Any | None = None
    message: dict | None = None


class DealsNextStepRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    deal: dict | None = None
    current_step: dict | None = None
    timeline: list | None = None
    messages: list | None = None
