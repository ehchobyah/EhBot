import configparser

PREFIX = "!"

# Читаем переменные из settings.ini
CONFIG = configparser.ConfigParser()
CONFIG.read("settings.ini")

# Создаем список эмодзи
with open('./emojis.txt', 'r', encoding='utf-8') as emoji_file:
    EMOJI_LIST = [line.strip() for line in emoji_file.readlines()]

# Создаем список флагов
with open('./flags.txt', 'r', encoding='utf-8') as flags_file:
    FLAG_LIST = [line.strip() for line in flags_file.readlines()]
