from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Literal

router = APIRouter(prefix="/targets", tags=["targets"])


class TargetCreate(BaseModel):
    name: str
    owner_user_id: str | None = None
    authorized: bool = False
    allowed_domains: list[str] = []
    allowed_ips: list[str] = []
    excluded_targets: list[str] = []
    allowed_ports: list[int] = []
    safe_mode: bool = True
    rate_limit_per_minute: int = 10
    request_budget: int = 2500
    time_limit_minutes: int = 240


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_target(payload: TargetCreate):
    return {
        "status": "created",
        "target": payload.model_dump(),
        "message": "Target created. Authorization and scope validation are required before active testing.",
    }


@router.get("/{target_id}")
async def get_target(target_id: str):
    return {"target_id": target_id, "status": "active"}
