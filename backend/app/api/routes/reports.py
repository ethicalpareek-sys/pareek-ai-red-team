from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("")
async def list_reports():
    return {"items": [], "count": 0}


@router.post("/generate")
async def generate_report():
    return {"status": "queued", "format": "json"}
