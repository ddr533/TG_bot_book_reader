# TG_bot_book_reader
Телеграм бот, который позволяет читать книгу в приложении.

#### Функции
* Постраничная пагинация
* Возможность сохранять закладки

#### Технологии
* Python==3.9
* aiogram==2.24
* sqlite3

#### Установка
* Клонировать репозиторий
  ```
  git clone https://github.com/ddr533/TG_bot_book_reader
  ```
* Cоздать и активировать виртуальное окружение на Windows:

```
python -m venv env
env/scripts/activate
```

* Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
* Записать свой токен от ТГ бота в файл .env
* Положить файл с книгой в папку book и назвать его book.txt
* Запустить бота bot.py




