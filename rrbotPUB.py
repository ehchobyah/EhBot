import hashlib
import random
import configparser
import json

import discord
from discord.ext import commands
from discord.utils import escape_mentions

# read replylist
with open("replyList.json", "r") as jsonFile:
    replyList = json.load(jsonFile)

# Читаем настройки из конфигурационного файла
config = configparser.ConfigParser()
config.read("settings.ini")  

# Создаем список эмодзи
with open('emojis.txt', 'r', encoding='utf-8') as emoji_file:
    emoji_list = [line.strip() for line in emoji_file.readlines()]
emoji_list_size = len(emoji_list)

# Создаем список флагов
with open('flags.txt', 'r', encoding='utf-8') as flags_file:
    flags_list = [line.strip() for line in flags_file.readlines()]
flags_list_size = len(flags_list)

# Настраиваем бота вместе с намереньями и префиксом
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_message_attachments(message):
    attachments = [i.url for i in message.attachments]
    return attachments

@bot.event
async def on_ready():
    '''Выводит имя бота при готовности'''
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    '''Обработчик входных сообщений'''
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        if not message.content.startswith('!'):
            # Экранируем упоминания
            content = escape_mentions(message.content)
            # Получаем хэш и эмодзи автора сообщения
            hash = int(hashlib.sha1(message.author.name.encode("utf-8")).hexdigest(), 16)
            emoj = hash % (10 ** 3) % emoji_list_size
            flag = hash % (10 ** 4) % flags_list_size
            # Отправляем сообщение в нужный канал
            channel = bot.get_channel(int(config['Server']['DVACH_CHANNEL_ID']))
            await channel.send(f'Аноним ({emoji_list[emoj]}:{flags_list[flag]}): {content}\n'+'\n'.join(get_message_attachments(message)))
    else:
        if message.author.guild_permissions.administrator and message.channel == bot.get_channel(int(config['Server']['PM_CHANNEL_ID'])):
            # Проверяем, что автор сообщения имеет права администратора
            await send_pm_to_author(message.author, message)

    await bot.process_commands(message)

@bot.command('randomrole')
async def randomrole(ctx):
    '''Присваивает случайную роль автору сообщения'''
    if ctx.channel == bot.get_channel(int(config['Server']['ROLE_CHANNEL_ID'])):
        await assign_random_role(ctx, ctx.author)

async def assign_random_role(ctx, member):
    '''Присваивает случайную роль выбранному участнику сервера'''
    server = member.guild
    user_roles = [role for role in member.roles if not (role.permissions.administrator or role.name == '@everyone')]
    try: 
        await member.remove_roles(*user_roles, reason='Снятие всех ролей перед присвоением новой роли')
    except:
        print(f'Не удалось удалить все роли у {member}')
    roles = [role for role in server.roles if not (role.permissions.administrator or role.name == '@everyone')]
    if roles:
        random_role = random.choice(roles)
    await member.add_roles(random_role)
    try: 
        await member.send(f'Поздравляю, вы получили роль: {random_role.name}')
    except:
        print(f'Не удалось отправить сообщение о получении роли {member}')
    await ctx.send(f'{ctx.author.mention}, ваша случайная роль: {random_role}')

@bot.command('pm')
async def pm(ctx):
    '''Отправляет вопрос в соответветствующий канал'''
    if isinstance(ctx.channel, discord.DMChannel):
        channel = bot.get_channel(int(config['Server']['PM_CHANNEL_ID']))
        content = escape_mentions(ctx.message.content)
        msg = await channel.send(f'**Вопрос**: {content}\n'+'\n'.join(get_message_attachments(ctx.message)))
        reply = {'msgId':msg.id,
                 'authorId':ctx.author.id}
        replyList.append(reply)
        with open("replyList.json", "w+") as jsonFile:
            json.dump(replyList, jsonFile)
            
async def send_pm_to_author(author, message):
    '''Отправляет ответ автору вопроса'''
    if message.reference is not None:
        replyMsgId = message.reference.message_id
        for reply in replyList:
            if reply['msgId'] == replyMsgId:
                user = await bot.fetch_user(reply['authorId'])
                await user.send(f'***Ответ от администратора:*** {message.content}\n'+'\n'.join(get_message_attachments(message)))

# Запускаем бота с токеном
bot.run(str(config['Bot']['TOKEN']))
