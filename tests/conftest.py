"""Shared fixtures and configuration for the test suite."""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from chemlab_api.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Provide an `AsyncClient` wired to the FastAPI app for the duration of a test

    The client comunicates with the app in-process via `ASGITransport`,
    so no actual network or server is involved.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
