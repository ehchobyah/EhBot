import json

import discord
from discord.ext import commands
from discord.utils import escape_mentions

from config import CONFIG, PREFIX, TEMP_ENV
from utils import get_message_attachments, dm_to_mentioned_user, replyList


class Messages(commands.Cog, name="Private message module"):
    ''' Messages module '''

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pm_channel = self.bot.get_channel(
            int(CONFIG['Server']['PM_CHANNEL_ID'])
        )
        self.template = TEMP_ENV.get_template('message.tpl')



    @commands.command()
    async def pm(self, ctx: commands.Context):
        """ Задай вопрос и жди ответа"""
        if isinstance(ctx.channel, discord.DMChannel):
            content = escape_mentions(ctx.message.content).replace('!pm','')
            msg = await self.pm_channel.send(await self.template.render_async( #type: ignore
                                                    sender='**Вопрос**',
                                                    content=content,
                                                    attachments=get_message_attachments(ctx.message)))
            # msg = await self.pm_channel.send(f'**Вопрос**: {content}\n'+'\n'.join(get_message_attachments(ctx.message)))
            reply = {'msgId':msg.id,
                    'authorId':ctx.author.id,
                    'msg': ctx.message.content.replace(f'{PREFIX}pm','')}
            replyList.append(reply)
            with open("replyList.json", "w+") as jsonFile:
                json.dump(replyList, jsonFile)

    @commands.Cog.listener()
    async def on_message(self, message):
        ''' Отлавливаем сообщение от админа в PM канале и отправляем как ответ '''
        if message.author == self.bot.user:
            return

        # Проверяем, что сообщение пришло в PM канал и автор имеет права админа
        elif (
            message.channel == self.pm_channel
            and
            message.author.guild_permissions.administrator
        ):
            await dm_to_mentioned_user(message,self.bot)


async def setup(bot: commands.Bot):
    await bot.add_cog(Messages(bot))
