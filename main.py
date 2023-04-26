import pathlib
import discord
from discord.ext import commands
from config import CONFIG, PREFIX

# Инициализируем бота вместе с намерениями
intents = discord.Intents.default()
intents.message_content = True
BOT = commands.Bot(command_prefix=PREFIX, intents=intents)


@BOT.event
async def on_ready():
    ''' Производит инициализацию '''
    print(f'Logged in as {BOT.user}')

    # Получаем список модулей соответствующей директории ./lib/commands и загружаем их
    modules = pathlib.Path(__file__).parent / "modules"
    for module in modules.iterdir():
        try:
            if pathlib.Path(module / "cog.py").exists():
                print(f"Loading module {module.name}")
                await BOT.load_extension(f"modules.{module.name}.cog")

        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load module {}\n{}".format(module, exc))

# Запускаем бота
BOT.run(str(CONFIG['Bot']['TOKEN']))
