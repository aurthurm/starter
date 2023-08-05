from asyncio import current_task
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from core.config import settings


@lru_cache(maxsize=None)
def get_sync_engine():
    return create_engine(settings.SQLALCHEMY_DATABASE_URI)


@lru_cache(maxsize=None)
def get_async_engine(*, echo=True):
    return create_async_engine(
        settings.SQLALCHEMY_TEST_ASYNC_DATABASE_URI
        if settings.TESTING
        else settings.SQLALCHEMY_ASYNC_DATABASE_URI,
        pool_pre_ping=True,
        echo=echo,
        future=True,
    )


def get_async_session():
    return sessionmaker(
        bind=get_async_engine(),
        expire_on_commit=False,
        autoflush=False,
        class_=AsyncSession,
    )


def get_async_session_scopped():
    return async_scoped_session(get_async_session(), scopefunc=current_task)
