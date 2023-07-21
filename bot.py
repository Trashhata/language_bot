import asyncio
import logging


from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu


# logger initiation
logger = logging.getLogger(__name__)


async def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Show info about bot start
    logging.info('Starting Bot')

    config: Config = load_config()

    # Bot and dispatcher initialization
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')

    await set_main_menu(bot)

    dp: Dispatcher = Dispatcher()

    # Routers connection
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Skip stocked updates
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

