from aiogram import Dispatcher
from aiogram.types import Message


def init_other_handlers(dp: Dispatcher):
    @dp.message_handler(content_types='text')
    async def send_echo(message: Message):
        """
        Этот хэндлер будет реагировать на любые текстовые
        сообщения пользователя.
        """
        await message.answer(f'Это эхо! {message.text}')
