import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from mydata_chatbot.configs import settings


engine: AsyncEngine = create_async_engine(
    settings.sqlite_url,
    echo=False,
    future=True,
    pool_pre_ping=True,
    # pool_size=5,
    # max_overflow=20,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

session: AsyncSession | async_scoped_session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=asyncio.current_task,
)


async def get_db_session():
    db = session()
    try:
        yield db
    except:
        await db.rollback()
        raise
    finally:
        await db.close()
