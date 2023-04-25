def get_message_attachments(message):
    ''' возвращает список прикрепленных к сообщению файлов '''
    attachments = [i.url for i in message.attachments]
    return attachments


async def dm_to_mentioned_user(message):
    ''' Отправляет ответ в личку пользователю, указанному в списке упоминаний '''
    if message.reference is not None:
        rep_message = await message.channel.fetch_message(message.reference.message_id)
        if (len(rep_message.mentions) == 1):
            channel = await rep_message.mentions[0].create_dm()
            await channel.send(f'Ответ от администратора: {message.content}\n'+'\n'.join(get_message_attachments(message)))
