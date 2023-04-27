from config import TEMP_ENV

import json

from discord.ext import commands

with open("replyList.json", "r") as jsonFile:
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
                
