import json

from discord.ext import commands

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


async def dm_to_mentioned_user(message,bot: commands.Bot):
    ''' Отправляет ответ в личку пользователю, указанному в списке упоминаний '''
    if message.reference is not None:
        replyMsgId = message.reference.message_id
        for reply in replyList:
            if reply['msgId'] == replyMsgId:
                user = await bot.fetch_user(reply['authorId'])
                await user.send(f'```{reply["msg"]}```\n***Ответ от администратора:*** {message.content}\n'+'\n'.join(get_message_attachments(message)))

