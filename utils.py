from config import TEMP_ENV


def get_message_attachments(message):
    ''' возвращает список прикрепленных к сообщению файлов '''
    attachments = [i.url for i in message.attachments]
    return attachments


async def dm_to_mentioned_user(message):
    ''' Отправляет ответ в личку пользователю, указанному в списке упоминаний '''
    template = TEMP_ENV.get_template('message.tpl')
    if message.reference is not None:
        rep_message = await message.channel.fetch_message(message.reference.message_id)
        if (len(rep_message.mentions) == 1):
            channel = await rep_message.mentions[0].create_dm()
            await channel.send(template.render( #type: ignore
                                    sender="Ответ от администратора",
                                    content=message.content,
                                    attachments=get_message_attachments(message)))
