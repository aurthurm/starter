from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_async_session, get_async_session_scopped


@asynccontextmanager
async def _get_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with _get_session() as session:
        yield session


@asynccontextmanager
async def session_scopped_context() -> Callable[
    ..., AbstractAsyncContextManager[AsyncSession]
]:
    session: Session = get_async_session_scopped()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        session.close()
