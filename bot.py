import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from database.database import init_db
from handlers.other_handlers import init_other_handlers
from handlers.user_handlers import init_user_handlers
from keyboards.main_menu import set_main_menu

# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main() -> None:
    '''Функция конфигурирования и запуска бота'''
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    config: Config = load_config('.env')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dispatcher: Dispatcher = Dispatcher(bot)

    # Инициализируем базу данных sqlite3
    init_db()

    # Настраиваем главное меню бота
    await set_main_menu(dispatcher)

    # Инициализируем хэндлеры
    init_user_handlers(dispatcher)
    init_other_handlers(dispatcher)

    # Запускаем polling
    try:
        await dispatcher.skip_updates()
        await dispatcher.start_polling()

    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        # Запускаем функцию main
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')
