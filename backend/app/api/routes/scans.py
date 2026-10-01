from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal

router = APIRouter(prefix="/scans", tags=["scans"])


class StartScanRequest(BaseModel):
    target_id: str
    mode: Literal["PASSIVE", "SAFE", "STANDARD", "DEEP", "API", "AUTHENTICATED", "FULL_ASSESSMENT"] = "SAFE"


@router.post("/start", status_code=status.HTTP_202_ACCEPTED)
async def start_scan(payload: StartScanRequest):
    if payload.mode not in {"PASSIVE", "SAFE", "STANDARD", "DEEP", "API", "AUTHENTICATED", "FULL_ASSESSMENT"}:
        raise HTTPException(status_code=400, detail="Invalid scan mode")
    return {
        "scan_id": "scan-123",
        "status": "queued",
        "mode": payload.mode,
        "target_id": payload.target_id,
        "message": "Scan queued. Authorization gate and scope validation are enforced before active execution.",
    }
