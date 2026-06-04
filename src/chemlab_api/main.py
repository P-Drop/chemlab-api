"""FastAPI application entry point."""

from fastapi import FastAPI

from chemlab_api.api.v1.router import api_router
from chemlab_api.core.config import settings

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(api_router, prefix="/api/v1")
