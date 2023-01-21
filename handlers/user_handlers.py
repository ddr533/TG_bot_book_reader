from __future__ import annotations

from copy import deepcopy

import aiogram
from aiogram.types import CallbackQuery, Message

from database import database
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book

LEN_BOOK: int = len(book)


def init_user_handlers(dp: aiogram.Dispatcher):
    @dp.message_handler(commands=['start'])
    async def process_start_command(message: Message):
        ''''
        Этот хэндлер будет срабатывать на команду "/start" -
        добавлять пользователя в базу данных, если его там еще не было
        и отправлять ему приветственное сообщение.
        '''
        database.add_user(message.from_user.id)
        await message.answer(LEXICON[message.text])


    @dp.message_handler(commands=['help'])
    async def process_help_command(message: Message):
        '''
        Этот хэндлер будет срабатывать на команду "/help"
        и отправлять пользователю сообщение со списком доступных команд в боте.
        '''
        await message.answer(LEXICON[message.text])


    @dp.message_handler(commands=['beginning'])
    async def process_beginning_command(message: Message):
        '''
        Этот хэндлер будет срабатывать на команду "/beginning"
        и отправлять пользователю первую страницу книги с кнопками пагинации.
        '''
        page: int = 1
        database.update_current_page(message.from_user.id, page)
        text: str = database.get_page_text(page)
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard('backward',
                                                    f'{page}/{LEN_BOOK}',
                                                    'forward'))


    @dp.message_handler(commands=['continue'])
    async def process_continue_command(message: Message):
        '''
        Этот хэндлер будет срабатывать на команду "continue"
        и отправлять пользователю страницу книги, на которой пользователь
        остановился в процессе взаимодействия с ботом.
        '''
        page = database.get_current_book_page(message.from_user.id)
        text = database.get_page_text(page)
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{page}/{LEN_BOOK}',
                'forward'))


    @dp.message_handler(commands=['bookmarks'])
    async def process_bookmarks_command(message: Message):
        '''
        Этот хэндлер будет срабатывать на команду "/bookmarks"
        и отправлять пользователю список сохраненных закладок,
        если они есть или сообщение о том, что закладок нет.
        '''
        bookmarks: list = database.get_bookmarks(message.from_user.id)
        if bookmarks:
            await message.answer(
                text=LEXICON[message.text],
                reply_markup=create_bookmarks_keyboard(*bookmarks))
        else:
            await message.answer(text=LEXICON['no_bookmarks'])


    @dp.callback_query_handler(text="forward")
    async def process_forward_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
        во время взаимодействия пользователя с сообщением-книгой.
        '''
        page: int = database.get_current_book_page(callback.from_user.id)
        if page < len(book):
            next_page: int = page + 1
            database.update_current_page(callback.from_user.id, next_page)
            text: str = database.get_page_text(next_page)
            await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{next_page}/{len(book)}',
                    'forward'))
        await callback.answer()


    @dp.callback_query_handler(text="backward")
    async def process_backward_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
        во время взаимодействия пользователя с сообщением-книгой
        '''
        page: int = database.get_current_book_page(callback.from_user.id)
        if page > 1:
            prev_page: int = page - 1
            database.update_current_page(callback.from_user.id, prev_page)
            text: str = database.get_page_text(prev_page)
            await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{prev_page}/{LEN_BOOK}',
                    'forward'))
        await callback.answer()


    @dp.callback_query_handler(lambda x: '/' in x.data and
                                         x.data.replace('/', '').isdigit())
    async def process_page_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
        с номером текущей страницы и добавлять текущую страницу в закладки.
        '''
        page: str = callback.data.split('/')[0]
        database.add_bookmark(callback.from_user.id, page)
        await callback.answer('Страница добавлена в закладки!')


    @dp.callback_query_handler(lambda x: x.data.isdigit())
    async def process_bookmark_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
        с закладкой из списка закладок.
        '''
        text: str = database.get_page_text(int(callback.data))
        database.update_current_page(callback.from_user.id, int(callback.data))
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{int(callback.data)}/{LEN_BOOK}',
                'forward'))
        await callback.answer()


    @dp.callback_query_handler(text="edit_bookmarks")
    async def process_edit_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
        "редактировать" под списком закладок.
        '''
        bookmarks: list = database.get_bookmarks(callback.from_user.id)
        await callback.message.edit_text(
            text=LEXICON[callback.data],
            reply_markup=create_edit_keyboard(*bookmarks))
        await callback.answer()


    @dp.callback_query_handler(text="cancel")
    async def process_cancel_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
        "отменить" во время работы со списком закладок
        (просмотр и редактирование).
        '''
        await callback.message.edit_text(text=LEXICON['cancel_text'])
        await callback.answer()


    @dp.callback_query_handler(lambda x: 'del' in x.data
                                         and x.data[:-3].isdigit())
    async def process_del_bookmark_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
        с закладкой из списка закладок к удалению.
        '''
        page_to_del: str = callback.data[:-3]
        database.remove_bookmark(callback.from_user.id, page_to_del)
        bookmarks: list = database.get_bookmarks(callback.from_user.id)
        if bookmarks:
            await callback.message.edit_text(
                text=LEXICON['/bookmarks'],
                reply_markup=create_edit_keyboard(*bookmarks))
        else:
            await callback.message.edit_text(text=LEXICON['no_bookmarks'])
        await callback.answer()


    @dp.message_handler(lambda x: x.text.isdigit() and
                                  1 <= int(x.text) <= LEN_BOOK)
    async def get_text_book_page(message: Message):
        '''
        Этот хэндлер будет срабатывать на ввод номера страницы.
        '''
        page: int = int(message.text)
        database.update_current_page(message.from_user.id, page)
        text = database.get_page_text(page)
        await message.delete()
        await message.answer(text=text,
                             reply_markup=create_pagination_keyboard(
                                            'backward',
                                            f'{page}/{LEN_BOOK}',
                                            'forward'))
