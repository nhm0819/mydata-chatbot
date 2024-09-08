import asyncio

# from sqlalchemy.ext.asyncio import async_scoped_session
from contextlib import asynccontextmanager
import contextlib

from mydata_chatbot.configs import settings
from mydata_chatbot.models import Base
from typing import AsyncIterator
from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base


# engine: AsyncEngine = create_async_engine(
#     settings.sqlite_url,
#     echo=False,
#     future=True,
#     pool_pre_ping=True,
#     # pool_size=5,
#     # max_overflow=20,
# )
#
# async_session_factory = async_sessionmaker(
#     bind=engine,
#     expire_on_commit=False,
#     class_=AsyncSession,
# )

# session: AsyncSession | async_scoped_session = async_scoped_session(
#     session_factory=async_session_factory,
#     scopefunc=asyncio.current_task,
# )
#
#
# async def get_db_session():
#     db = session()
#     try:
#         yield db
#     except:
#         await db.rollback()
#         raise
#     finally:
#         await db.close()



class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_async_engine(
            settings.sqlite_url,
            echo=False,
            future=True,
            pool_pre_ping=True,
            # pool_size=5,
            # max_overflow=20,
        )
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


sessionmanager = DatabaseSessionManager()

async def get_session():
    async with sessionmanager.session() as session:
        yield session
