"""Async SQLAlchemy engine and per-request session management."""

from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from chemlab_api.core.config import settings

engine = create_async_engine(settings.database_url, pool_pre_ping=True)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session per request, closed on exit"""
    async with async_session_factory() as session:
        yield session


async def check_database_connection() -> None:
    """Verify the database is reachable by runnig a trivial query."""
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))


async def dispose_engine() -> None:
    """Dispose of the engine's connection pool (called on shutdown)."""
    await engine.dispose()
