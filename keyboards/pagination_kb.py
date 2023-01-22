from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon import LEXICON


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    '''Функция, генерирующая клавиатуру для страницы книги.'''
    # Создаем объект клавиатуры
    pagination_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
    # Наполняем клавиатуру кнопками
    pagination_kb.row(*[InlineKeyboardButton(LEXICON[button]
                                             if button in LEXICON else button,
                      callback_data=button) for button in buttons])
    return pagination_kb
