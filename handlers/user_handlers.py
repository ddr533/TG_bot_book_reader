from copy import deepcopy
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from database.database import user_dict_template, users_db
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book


def init_user_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def process_start_command(message: Message):
        ''''
        Этот хэндлер будет срабатывать на команду "/start" -
        добавлять пользователя в базу данных, если его там еще не было
        и отправлять ему приветственное сообщение.
        '''
        await message.answer(LEXICON[message.text])
        if message.from_user.id not in users_db:
            users_db[message.from_user.id] = deepcopy(user_dict_template)

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
        users_db[message.from_user.id]['page'] = 1
        text = book[users_db[message.from_user.id]['page']]
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                'forward'))

    @dp.message_handler(commands=['continue'])
    async def process_continue_command(message: Message):
        '''
        Этот хэндлер будет срабатывать на команду "continue"
        и отправлять пользователю страницу книги, на которой пользователь
        остановился в процессе взаимодействия с ботом
        '''
        text = book[users_db[message.from_user.id]['page']]
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                'forward'))

    @dp.message_handler(commands=['bookmarks'])
    async def process_bookmarks_command(message: Message):
        '''
        Этот хэндлер будет срабатывать на команду "/bookmarks"
        и отправлять пользователю список сохраненных закладок,
        если они есть или сообщение о том, что закладок нет.
        '''
        if users_db[message.from_user.id]["bookmarks"]:
            await message.answer(
                text=LEXICON[message.text],
                reply_markup=create_bookmarks_keyboard(
                    *users_db[message.from_user.id]["bookmarks"]))
        else:
            await message.answer(text=LEXICON['no_bookmarks'])

    @dp.callback_query_handler(text="forward")
    async def process_forward_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
        во время взаимодействия пользователя с сообщением-книгой.
        '''
        if users_db[callback.from_user.id]['page'] < len(book):
            users_db[callback.from_user.id]['page'] += 1
            text = book[users_db[callback.from_user.id]['page']]
            await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
        await callback.answer()

    @dp.callback_query_handler(text="backward")
    async def process_backward_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
        во время взаимодействия пользователя с сообщением-книгой
        '''
        if users_db[callback.from_user.id]['page'] > 1:
            users_db[callback.from_user.id]['page'] -= 1
            text = book[users_db[callback.from_user.id]['page']]
            await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
        await callback.answer()

    @dp.callback_query_handler(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
    async def process_page_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
        с номером текущей страницы и добавлять текущую страницу в закладки.
        '''
        users_db[callback.from_user.id]['bookmarks'].add(
            users_db[callback.from_user.id]['page'])
        await callback.answer('Страница добавлена в закладки!')

    @dp.callback_query_handler(lambda x: x.data.isdigit())
    async def process_bookmark_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
        с закладкой из списка закладок.
        '''
        text = book[int(callback.data)]
        users_db[callback.from_user.id]['page'] = int(callback.data)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'))
        await callback.answer()

    @dp.callback_query_handler(text="edit_bookmarks")
    async def process_edit_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
        "редактировать" под списком закладок.
        '''
        await callback.message.edit_text(
            text=LEXICON[callback.data],
            reply_markup=create_edit_keyboard(
                *users_db[callback.from_user.id]["bookmarks"]))
        await callback.answer()

    @dp.callback_query_handler(text="cancel")
    async def process_cancel_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
        "отменить" во время работы со списком закладок (просмотр и редактирование).
        '''
        await callback.message.edit_text(text=LEXICON['cancel_text'])
        await callback.answer()

    @dp.callback_query_handler(lambda x: 'del' in x.data and x.data[:-3].isdigit())
    async def process_del_bookmark_press(callback: CallbackQuery):
        '''
        Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
        с закладкой из списка закладок к удалению.
        '''
        users_db[callback.from_user.id]['bookmarks'].remove(
            int(callback.data[:-3]))
        if users_db[callback.from_user.id]['bookmarks']:
            await callback.message.edit_text(
                text=LEXICON['/bookmarks'],
                reply_markup=create_edit_keyboard(
                    *users_db[callback.from_user.id]["bookmarks"]))
        else:
            await callback.message.edit_text(text=LEXICON['no_bookmarks'])
        await callback.answer()