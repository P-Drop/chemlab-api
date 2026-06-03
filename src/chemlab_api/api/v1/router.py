"""Aggregator for all v1 API routers."""

from fastapi import APIRouter

from chemlab_api.api.v1.endpoints import health

api_router = APIRouter()

api_router.include_router(router=health.router)
