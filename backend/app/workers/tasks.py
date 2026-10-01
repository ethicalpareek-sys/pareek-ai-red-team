from celery import shared_task


@shared_task
def run_scan_task(target_id: str, mode: str = "SAFE"):
    return {
        "target_id": target_id,
        "mode": mode,
        "status": "queued",
        "message": "Protected scan task accepted for execution.",
    }
