''' работа с базами данных '''
from __future__ import annotations

import sqlite3

from services.file_handling import book


def init_db() -> None:
    ''' инициализация базы данных '''
    with sqlite3.connect('sqlite3') as con:
        cur = con.cursor()
        cur.executescript('''
                          CREATE TABLE IF NOT EXISTS users_db (
                          user_id INTEGER PRIMERY KEY UNIQUE,
                          page INTEGER,
                          bookmarks TEXT);
                          CREATE TABLE IF NOT EXISTS book (
                          page INTEGER PRIMERY KEY,
                          text TEXT);
                          ''')
        if not check_book_db():
            cur.execute('DELETE FROM book')
            cur.executemany('INSERT INTO book(page, text) VALUES(?,?)',
                            book.items())
    con.close()


def check_book_db() -> bool:
    ''' проверка базы book '''
    with sqlite3.connect('sqlite3') as con:
        cur = con.cursor()
        cur.execute('SELECT page FROM book')
        res = cur.fetchall()
    con.close()
    return len(res) == len(book)


def add_user(user_id: int) -> None:
    ''' добавление пользователя '''
    with sqlite3.connect('sqlite3') as con:
        cur = con.cursor()
        cur.execute(f'SELECT user_id FROM users_db WHERE user_id == {user_id}')
        res = cur.fetchall()
        if not res:
            cur.execute('INSERT INTO users_db(user_id, page)'
                        'VALUES(?,?)',
                        (user_id, 1))
    con.close()


def get_page_text(page: int) -> str:
    ''' получение страницы '''
    with sqlite3.connect('sqlite3') as con:
        cur = con.cursor()
        cur.execute('SELECT text '
                    'FROM book '
                    'WHERE page == :Page',
                    {'Page': page})
        text: str = cur.fetchone()[0]
    con.close()
    return text


def get_current_book_page(user_id: int) -> int:
    ''' получение текущей страницы книги '''
    with sqlite3.connect('sqlite3') as con:
        cur = con.cursor()
        cur.execute('SELECT page FROM users_db WHERE user_id == :User',
                    {'User': user_id})
        page: int = cur.fetchone()[0]
    con.close()
    return page


def update_current_page(user_id: int, page: int) -> None:
    ''' обновление текущей страницы '''
    with sqlite3.connect('sqlite3') as con:
        cur = con.cursor()
        cur.execute('UPDATE users_db '
                    'SET page = :Page '
                    'WHERE user_id == :User',
                    {'Page': page, 'User': user_id})
    con.close()


def get_bookmarks(user_id: int) -> list[int]:
    ''' получение закладок '''
    with sqlite3.connect('sqlite3') as con:
        cur = con.cursor()
        cur.execute('SELECT bookmarks FROM users_db WHERE user_id == :User_id',
                    {'User_id': user_id})
        bookmarks: str = cur.fetchone()[0]
        marks_lst: list[int] = ([int(x) for x in bookmarks.split(',') if x]
                                if bookmarks else [])
    con.close()
    return marks_lst


def add_bookmark(user_id: int, page: str) -> None:
    ''' вставить закладку '''
    bookmarks: list = get_bookmarks(user_id)
    if int(page) not in bookmarks:
        bookmarks.append(int(page))
        bookmarks_new: str = ','.join([str(x) for x in bookmarks])
        update_bookmarks(bookmarks_new, user_id)


def remove_bookmark(user_id: int, page: str) -> None:
    ''' удалить закладку '''
    bookmarks: list = get_bookmarks(user_id)
    bookmarks.remove(int(page))
    bookmarks_new: str = ','.join([str(x) for x in bookmarks])
    update_bookmarks(bookmarks_new, user_id)


def update_bookmarks(bookmarks_new: str, user_id):
    ''' обновить закладку '''
    with sqlite3.connect('sqlite3') as con:
        cur = con.cursor()
        cur.execute('UPDATE users_db '
                    'SET bookmarks = :Bookmarks_new '
                    'WHERE user_id == :User_id',
                    {'User_id': user_id, 'Bookmarks_new': bookmarks_new})
    con.close()
