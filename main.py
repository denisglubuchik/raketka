import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import settings
from handlers import router
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    bot = Bot(token=settings.token, default=DefaultBotProperties(parse_mode='HTML'))

    storage = RedisStorage.from_url(settings.redis)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
