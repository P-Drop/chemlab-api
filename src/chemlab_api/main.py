"""FastAPI application entry point."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from chemlab_api.api.v1.router import api_router
from chemlab_api.core.config import settings
from chemlab_api.db.session import check_database_connection, dispose_engine

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await check_database_connection()
    logger.info("Database connection verified")
    yield
    await dispose_engine()


app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")
