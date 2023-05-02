import configparser
from jinja2 import Environment,FileSystemLoader

from datetime import tzinfo
from datetime import timedelta

PREFIX = "!"

# Читаем переменные из settings.ini
CONFIG = configparser.ConfigParser()
CONFIG.read("settings.ini")

# Создаем список эмодзи
with open('./emojis.txt', 'r', encoding='utf-8') as emoji_file:
    EMOJI_LIST = [line.strip() for line in emoji_file.readlines()]

# Загрузка окружения для темплейтов
TEMP_ENV = Environment(loader=FileSystemLoader('templates'),enable_async=True)

# Создаем список аватаров
with open('./avatars.txt', 'r', encoding='utf-8') as flags_file:
    AVATAR_LIST = [line.strip() for line in flags_file.readlines()]

class MSK(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=3)

    def dst(self, dt):
        return timedelta(seconds=0)

    def tzname(self, dt):
        return 'KST'

    def __repr__(self):
        return f'<{self.__class__.__name__}+03:00>'
