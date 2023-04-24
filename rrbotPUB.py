import discord
import hashlib
from discord.ext import commands
import random
from discord.utils import escape_mentions

# Создаем список привилегированных намерений
intents = discord.Intents.default()
intents.message_content = True

# Создаем экземпляр бота с указанием префикса и привилегированных намерений
bot = commands.Bot(command_prefix='!', intents=intents)

DVACH_CHANNEL_ID = id  # Замените на ID канала, в который нужно перенаправлять сообщения
PM_CHANNEL_ID = id  # Замените на ID канала, в который нужно перенаправлять сообщения

emoji_list = [
    '😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', '🙃', '😉', '😊', '😇',
    '😍', '🥰', '😘', '😗', '😚', '😙', '😋', '😛', '😜', '😝', '🤑', '🤗', '🤔',
    '🤐', '🤨', '😐', '😑', '😶', '😏', '😒', '🙄', '😬', '🤥', '😌', '😔', '😪',
    '🤤', '😴', '😷', '🤒', '🤕', '🤢', '🤮', '🤧', '😵', '🥵', '🥶', '😎', '🤓',
    '🧐', '😕', '😟', '🙁', '☹️', '😮', '😯', '😲', '😳', '🥺', '😦', '😧', '😨',
    '😰', '😥', '😢', '😭', '😱', '😖', '😣', '😞', '😓', '😩', '😫', '🥱', '😤',
    '😡', '😠', '🤬', '😈', '👿', '💀', '☠️', '💩', '🤡', '👹', '👺', '👻', '👽',
    '👾', '🤖', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾', '🐵', '🦍',
    '🐶', '🐕', '🦮', '🐕‍🦺', '🐩', '🐺', '🦊', '🦝', '🐱', '🐈', '🦁', '🐯', '🐅',
    '🐆', '🐴', '🐎', '🦄', '🦓', '🦌', '🐮', '🐂', '🐃', '🐄', '🐷', '🐖', '🐗',
    '🐽', '🐏', '🐑', '🐐', '🐪', '🐫', '🦙', '🦒', '🐘', '🦏', '🦛', '🐭', '🐁',
    '🐀', '🐹', '🐰', '🐇', '🐿', '🦔', '🦇', '🐻', '🐨', '🐼', '🦥', '🦦', '🦨',
    '🦩', '🦜', '🦢', '🦆', '🦉', '🦚', '🦆', '🦔', '🐢', '🐍', '🦕', '🦖', '🐊', '🐸',
    '🦓', '🐆', '🐅', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦙', '🦒', '🦘', '🐃',
    '🐄', '🐂', '🐎', '🐖', '🐗', '🐏', '🐑', '🐐', '🐓', '🦃', '🦜', '🦢', '🦜', '🐀',
    '🐁', '🐿', '🦔', '🐇', '🐰', '🐿', '🦦', '🐉', '🐲', '🌵', '🎄', '🌲', '🌳', '🌴',
    '🌱', '🌿', '☘️', '🍀', '🎍', '🎋', '🍃', '🍂', '🍁', '🍄', '🐚', '🌾', '💐', '🌷',
    '🌹', '🥀', '🌺', '🌸', '🌼', '🌻', '🌞', '🌝', '🌛', '🌜', '🌚', '🌕', '🌖', '🌗',
    '🌘', '🌑', '🌒', '🌓', '🌔', '🌙', '🌎', '🌍', '🌏', '💫', '⭐️', '🌟', '✨', '💥',
    '🔥', '🌪', '🌈', '☀️', '🌤', '⛅️', '🌥', '☁️', '🌦', '🌧', '⛈', '🌩', '❄️',
    '🌨', '🌬', '💨', '🌊', '💧', '💦', '☔️', '🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉',
    '🍇', '🍓', '🍈', '🍒', '🍑', '🍍', '🥝', '🥑', '🍅', '🍆', '🥔', '🥕', '🌽', '🌶',
    '🥒', '🥬', '🥦', '🧄', '🧅', '🍄', '🥜', '🌰', '🍞', '🥐', '🥖',
    '🥨', '🥞', '🧇', '🧀', '🍖', '🍗', '🥩', '🥓', '🍔', '🍟', '🍕', '🌭', '🥪', '🌮',
    '🌯', '🥙', '🍱', '🍲', '🍛', '🍜', '🍝', '🍠', '🍢', '🍣', '🍤', '🍥', '🥮', '🍡',
    '🥟', '🥠', '🥡', '🍦', '🍧', '🍨', '🍩', '🍪', '🎂', '🍰', '🧁', '🥧', '🍫', '🍬',
    '🍭', '🍮', '🍯', '🍼', '🥛', '☕️', '🍵', '🍶', '🍾', '🍷', '🍸', '🍹', '🍺', '🍻',
    '🥂', '🥃', '🥤', '🧊'
]
emoji_lut_size = len(emoji_list)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        if not message.content.startswith('!pm'):
            content = escape_mentions(message.content)  # Экранируем упоминания
            channel = bot.get_channel(DVACH_CHANNEL_ID)
            hash = int(hashlib.sha1(message.author.name.encode("utf-8")).hexdigest(), 16)
            emoj = hash % (10 ** 3) % emoji_lut_size
            await channel.send(f'Аноним ({hash % (10 ** 4)}:{emoji_list[emoj]}): {content}')
    else:
        if message.author.guild_permissions.administrator and message.channel == bot.get_channel(PM_CHANNEL_ID):
            # Проверяем, что автор сообщения имеет права администратора
            print('right')
            await send_pm_to_author(message.author, message)

    await bot.process_commands(message)

@bot.command()
async def randomrole(ctx):
    if ctx.channel.name == '🤠получи-роль🥳':
        await assign_random_role(ctx, ctx.author)

@bot.command()
async def pm(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        channel = bot.get_channel(PM_CHANNEL_ID)
        content = escape_mentions(ctx.message.content)
        await channel.send(f'**Вопрос от {ctx.author.mention}: {content}')
async def send_pm_to_author(author, message):
    if message.reference is not None:
        print('super!')
        rep_message = await message.channel.fetch_message(message.reference.message_id)
        if(len(rep_message.mentions) == 1):
            channel = await rep_message.mentions[0].create_dm()
            await channel.send(f'Ответ от администратора: {message.content}')


async def assign_random_role(ctx, member):
    server = member.guild
    user_roles = [role for role in member.roles if not (role.permissions.administrator or role.name == '@everyone')]
    await member.remove_roles(*user_roles, reason='Снятие всех ролей перед присвоением новой роли')
    roles = [role for role in server.roles if not (role.permissions.administrator or role.name == '@everyone')]
    if roles:
        random_role = random.choice(roles)
    await member.add_roles(random_role)
    await member.send(f'Поздравляю, вы получили роль: {random_role.name}')
    await ctx.send(f'{ctx.author.mention}, ваша случайная роль: {random_role}')

# Запускаем бота с токеном
bot.run('bot token')  # Вставляем токен своего бота
