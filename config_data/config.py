from dataclasses import dataclass
from typing import Union

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: Union[str, None]) -> Config:
    '''Функция читает файл .env и возвращает экземпляр класса Config.'''
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS')))))
