import logging.config

from mydata_chatbot import database
from mydata_chatbot import models
from mydata_chatbot.configs import settings as default_settings

logger = logging.getLogger(__name__)


async def startup_event_1():
    logger.info(f"Default Params:")
    for key, value in default_settings.dict().items():
        logger.info(f"  {key}: {value}")


async def startup_event_2():
    logger.info("Synchronizing databases..")
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def shutdown_event():
    logger.info("shutting down..")
    await database.engine.dispose()
