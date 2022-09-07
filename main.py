"""
BotApp
Application
"""

import asyncio
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import Bot, Dispatcher, types
from beanie import init_beanie
from bot_app.confmaker import config
from bot_app.models import __beanie_models__
from bot_app.core import db, logger
from bot_app.filters import UserRegisteredFilter
from bot_app.middleware.getlocale import GetLocaleMiddleware
from bot_app.handlers import *


async def start():
    """
    SlagBot
    Entry point
    """

    # Setup beanie models
    await init_beanie(db, document_models=__beanie_models__)

    # Setup bot
    storage = RedisStorage2(host=config['redis']['host'],
                            port=config['redis']['port'],
                            password=config['redis']['pwd'],
                            db=config['redis']['db'])
    bot = Bot(token=config['telegram']['token'])
    dp = Dispatcher(bot, storage=storage)

    # Setup bot middleware
    getlocale = GetLocaleMiddleware(fallback='en')
    dp.setup_middleware(getlocale)

    # Setup bot filters
    dp.filters_factory.bind(UserRegisteredFilter)

    # Setup bot handlers
    register_handlers_common(dp)
    register_handlers_registration(dp)
    register_handlers_locale(dp)

    # Start bot
    try:
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Bot stopped')
