from discord.ext import commands
from config import CONFIG, DRIVER

from selenium.webdriver.common.by import By

import asyncio 

from datetime import datetime

class Unbanned(commands.Cog,name="Is Vanja Unbanned?"):
    ''' Узнай разбанили ли ваню или нет? '''

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.unbanned_channel = self.bot.get_channel(
                int(CONFIG['Server']['UNBANNED_CHANNEL_ID']))
        self.url = CONFIG['Server']['TWITCH_URL']
        asyncio.create_task(self.checker())

    @commands.command(aliases = ['un','ban','banned','isbanned','че там с ним','u'])
    async def unbanned(self, ctx: commands.Context):
        ''' Узнает разбанили ли ваню '''
        if await find_is_channel_unbanned(self.url):
            await ctx.channel.send("РАЗБАНИЛИИ")
        else:
            await ctx.channel.send("Ваню не разбанили😔😭")

    async def checker(self):
        while True:
            await asyncio.sleep(300)
            time_now = datetime.now().strftime("%d-%m-%Y %H:%M")
            if await find_is_channel_unbanned(self.url):
               await self.unbanned_channel.send(f"На момент {time_now}(мск) Ваню РАЗБАНИЛИИ🥳🥳🥳🥳") 
            else:
               await self.unbanned_channel.send(f"На момент {time_now}(мск) Ваня все еще в бане😞😔😭😭") 


async def find_is_channel_unbanned(url):
    DRIVER.get(url)
    try:
        p_channel_banned = DRIVER.find_element(by=By.CLASS_NAME, value='kQmXqp')
        return False
    except Exception:
        return True

async def setup(bot: commands.Bot):
    await bot.add_cog(Unbanned(bot))
