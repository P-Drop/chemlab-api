"""Tests for the /health endpoint."""

from http import HTTPStatus

from httpx import AsyncClient


async def test_health_check_returns_200_status_code(client: AsyncClient) -> None:
    """The /health endpoint should respond with HTTP 200."""

    # Act
    response = await client.get("/api/v1/health")

    # Assert
    assert response.status_code == HTTPStatus.OK


async def test_health_check_returns_status_ok_payload(client: AsyncClient) -> None:
    """The /health endpoint should respond with the expedted payload."""

    # Act
    response = await client.get("/api/v1/health")

    # Assert
    assert response.json() == {"status": "ok"}
