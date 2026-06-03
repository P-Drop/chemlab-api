"""Health check endpoint."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["Health"])


class HealthResponse(BaseModel):
    """Response schema for the health check endpoint."""

    status: Literal["ok"]


@router.get(
    "",
    response_model=HealthResponse,
    summary="Service health check",
    description=(
        "Return the operational status of the API. "
        "Intended for use by orchestators, load balancers and uptime monitors."
    ),
)
async def health_check() -> HealthResponse:
    """Return the current health status of the service."""
    return HealthResponse(status="ok")
