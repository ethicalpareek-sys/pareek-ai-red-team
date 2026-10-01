from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes.targets import router as targets_router
from app.api.routes.scans import router as scans_router
from app.api.routes.findings import router as findings_router
from app.api.routes.reports import router as reports_router
from app.core.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="PAREEK AI RED TEAM",
    version="1.0.0",
    description="Authorized AI-powered web app security assessment platform",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(targets_router, prefix="/api/v1")
app.include_router(scans_router, prefix="/api/v1")
app.include_router(findings_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")


@app.get("/health")
async def healthcheck():
    return {"status": "ok", "app": settings.app_name}
