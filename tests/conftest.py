import logging.config

import pytest
import pytest_asyncio
import yaml
import asyncio
from httpx import AsyncClient

import directories
from mydata_chatbot import database, models

logger = logging.getLogger(__name__)

from mydata_chatbot.database import session, engine


async def get_db_session():
    db = session()
    try:
        yield db
    except:
        await db.rollback()
        raise
    finally:
        await db.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_logging_configs(request):
    """Cleanup a testing directory once we are finished."""
    with open(directories.logging, "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
        logging.config.dictConfig(config)


@pytest.fixture(scope="session", autouse=True)
def setup_lifecycle(request):
    def finalizer():
        logger.debug("Shutting down unittest session..")

    request.addfinalizer(finalizer)


@pytest_asyncio.fixture(scope="session")
async def client():
    from mydata_chatbot.apps.v1 import app

    async with AsyncClient(app=app, base_url="http://test") as a_client:
        print("Creating a client..")
        yield a_client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_and_drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        logger.debug("Database created.")
    yield
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        logger.debug("Database dropped.")
