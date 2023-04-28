import configparser
from jinja2 import Environment,FileSystemLoader

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

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

# Установим селениум драйвер
WEBDRIVER_OPTIONS = webdriver.ChromeOptions()
WEBDRIVER_OPTIONS.add_argument('headless')
DRIVER = webdriver.Chrome(service=ChromeService(
         ChromeDriverManager().install()),options=WEBDRIVER_OPTIONS)
DRIVER.implicitly_wait(0.5)
