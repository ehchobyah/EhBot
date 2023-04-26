import discord
from discord.ext import commands
from discord.utils import escape_mentions

from config import CONFIG,TEMP_ENV
from utils import get_message_attachments, dm_to_mentioned_user


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
            content = escape_mentions(ctx.message.content)
            await self.pm_channel.send(self.template.render( #type: ignore
                                sender=f'**Вопрос от {ctx.author.mention}**',
                                content=content,
                                attachments=get_message_attachments(ctx.message))) 
           

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
            await dm_to_mentioned_user(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(Messages(bot))
