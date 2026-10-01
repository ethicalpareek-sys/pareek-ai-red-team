from fastapi import APIRouter, status

router = APIRouter(prefix="/findings", tags=["findings"])


@router.get("")
async def list_findings():
    return {"items": [], "count": 0}


@router.get("/{finding_id}")
async def get_finding(finding_id: str):
    return {"finding_id": finding_id, "status": "not_found"}
