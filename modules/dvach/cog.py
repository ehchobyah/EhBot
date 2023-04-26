import discord
from discord.utils import escape_mentions
from discord.ext import commands
import discord_webhook
import hashlib

from config import CONFIG, EMOJI_LIST, AVATAR_LIST, PREFIX
from utils import get_message_attachments, dm_to_mentioned_user


class Dvach(commands.Cog, name="2ch"):
    """ 2ch module """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Получаем канал PM и DVACH
        self.pm_channel = self.bot.get_channel(
            int(CONFIG['Server']['PM_CHANNEL_ID'])
        )
        self.dvach_channel = self.bot.get_channel(
            int(CONFIG['Server']['DVACH_CHANNEL_ID'])
        )
        self.dvach_webhook = str(CONFIG['Server']['DVACH_CHANNEL_WEBHOOK'])

    @commands.Cog.listener()
    async def on_message(self, message):
        '''Обработчик входных сообщений'''
        if message.author == self.bot.user:
            return

        # Если сооббщение поступило в личку бота и без префикса, оно перенаправляется в 2ch
        if isinstance(message.channel, discord.DMChannel):
            if not message.content.startswith(PREFIX):
                # экранируем упоминания
                content = escape_mentions(message.content)
                # Хэшируем имя пользователя и присваеваем ему псевдоним
                salt = int(CONFIG['Bot']['SALT'])
                hash = int(hashlib.sha1(str(message.author.id^salt).encode("utf-8")).hexdigest(), 16)
                emoji = EMOJI_LIST[hash % (10 ** 3) % len(EMOJI_LIST)]
                webhook_username = str(hash % (10 ** 4)) + emoji
                webhook_avatar = AVATAR_LIST[hash % (10 ** 3) % len(AVATAR_LIST)]
                webhook = discord_webhook.DiscordWebhook(url=self.dvach_webhook, username=webhook_username, avatar_url=webhook_avatar)
                webhook.content = content + '\n' + '\n'.join(get_message_attachments(message))
                # Отправляем сообщение в 2ch канал
                webhook.execute()


async def setup(bot: commands.Bot):
    await bot.add_cog(Dvach(bot))
