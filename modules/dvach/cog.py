import discord
from discord.ext import commands


from config import CONFIG, PREFIX, TEMP_ENV
from utils import get_message_attachments, dm_to_mentioned_user, sendWebhook


class Dvach(commands.Cog, name="2ch"):
    """ 2ch module """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Получаем канал PM и DVACH
        self.pm_channel = self.bot.get_channel(
            int(CONFIG['Server']['PM_CHANNEL_ID'])
        )
        self.dvach_category = int(CONFIG['Server']['DVACH_CATEGORY_ID'])
        self.template = TEMP_ENV.get_template('message.tpl')
        self.dvach_webhook = str(CONFIG['Server']['DVACH_CHANNEL_WEBHOOK'])


    @commands.command()
    async def new(self, ctx: commands.Context):
        """ Создание нового треда """
        if isinstance(ctx.channel, discord.DMChannel):
            guild = self.bot.get_guild(self.pm_channel.guild.id)
            category = discord.utils.get(guild.categories, id=self.dvach_category)
            content = ctx.message.content.replace(f'{PREFIX}new','')
            if content != '':
                if len(category.channels) == int(CONFIG['Dvach']['THREAD_LIMIT']):
                    await category.channels[len(category.channels)-1].delete()
                channel = await guild.create_text_channel(content,
                                                          category=category,
                                                          overwrites={guild.default_role: discord.PermissionOverwrite(send_messages=False)})
                await channel.move(beginning=True)
                await channel.create_webhook(name='2ch')
                webhooks = await channel.webhooks()
                await sendWebhook(ctx.message,webhooks[0].url,f'{content}\n||*Номер треда: {channel.id}*||')
                await ctx.channel.send(f'Тред созднан✅')


    @commands.command()
    async def send(self, ctx: commands.Context):
        """ Вывести треды для ответа """
        if isinstance(ctx.channel, discord.DMChannel):
            guild = self.bot.get_guild(self.pm_channel.guild.id)
            category = discord.utils.get(guild.categories, id=self.dvach_category)
            channels = category.text_channels
            await ctx.channel.send('**Выбери куда отправляем сообщение?**\nПросто отправь реплай с тредом, в который ты хочешь написать.')
            for channel in channels:
                await ctx.channel.send(f':zap:Тред: {channel}\n{channel.jump_url}\n{channel.id}',suppress_embeds=True)


    @commands.Cog.listener()
    async def on_message(self, message):
        '''Обработчик входных сообщений'''
        if message.author == self.bot.user:
            return
        if isinstance(message.channel, discord.DMChannel): 
            if not message.content.startswith(PREFIX):
                try:
                    msgReference = message.reference.resolved.content
                    id = int(msgReference.split()[len(msgReference.split())-1])
                    channel = self.bot.get_channel(id)
                    webhooks = await channel.webhooks()
                    await sendWebhook(message,
                                      webhooks[0].url,
                                      message.content)
                    countMessages = len([message async for message in channel.history(limit=int(CONFIG['Dvach']['BUMP_LIMIT'])+1)])
                    if countMessages <= int(CONFIG['Dvach']['BUMP_LIMIT']):
                        await channel.move(beginning=True)
                except:
                    await message.channel.send('Oops.. Ошибочка...')


async def setup(bot: commands.Bot):
    await bot.add_cog(Dvach(bot))
