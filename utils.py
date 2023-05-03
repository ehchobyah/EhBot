from config import TEMP_ENV, CONFIG, EMOJI_LIST, AVATAR_LIST

import json
import hashlib

from discord.ext import commands
from discord.utils import escape_mentions
import discord_webhook


'''чтение файла с вопросами '''
try:
    with open("replyList.json", "r") as jsonFile:
        replyList = json.load(jsonFile)

except:
    '''создание файла с вопросами, если его не было '''
    with open("replyList.json", "w+") as jsonFile:
        jsonFile.write('[]')
        replyList = json.load(jsonFile)

def get_message_attachments(message):
    ''' возвращает список прикрепленных к сообщению файлов '''
    attachments = [i.url for i in message.attachments]
    return attachments


async def dm_to_mentioned_user(message, bot: commands.Bot):
    ''' Отправляет ответ в личку пользователю, указанному в списке упоминаний '''
    template = TEMP_ENV.get_template('message.tpl')
    if message.reference is not None:
        replyMsgId = message.reference.message_id
        try:
            reply = list(filter(lambda reply: reply['msgId']==replyMsgId,replyList))[0]
            user = await bot.fetch_user(reply['authorId'])
            await user.send(await template.render_async(
                                      reply=reply["msg"],
                                      sender="***Ответ от администратора***",
                                      content=message.content,
                                      attachments=get_message_attachments(message)))
       
            del replyList[replyList.index(reply)]
            with open("replyList.json", "w") as file:
                file.write(json.dumps(replyList))
        except Exception:
            print('Ошибка! Вы уже отвечали на этот вопрос.')

async def sendWebhook(message,webhookURL,content):
        template = TEMP_ENV.get_template('message.tpl')
        # Хэшируем имя пользователя и присваеваем ему псевдоним
        salt = int(CONFIG['Bot']['SALT'])
        hash = int(hashlib.sha1(str(message.author.id^salt).encode("utf-8")).hexdigest(), 16)
        emoji = EMOJI_LIST[hash % (10 ** 3) % len(EMOJI_LIST)]
        webhook_username = str(hash % (10 ** 4)) + emoji
        webhook_avatar = AVATAR_LIST[hash % (10 ** 3) % len(AVATAR_LIST)]
        webhook = discord_webhook.DiscordWebhook(url=webhookURL,
                                                 username=webhook_username,
                                                 avatar_url=webhook_avatar)
        webhook.content = await template.render_async( #type: ignore
                            content=content,
                            attachments=get_message_attachments(message))
               
        webhook.execute()