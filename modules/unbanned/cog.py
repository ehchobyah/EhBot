from discord.ext import commands
from config import CONFIG

import asyncio 
from aiohttp import ClientSession

from datetime import datetime

class Unbanned(commands.Cog,name="Is Vanja Unbanned?"):
    ''' Узнай разбанили ли ваню или нет? '''

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.unbanned_channel = self.bot.get_channel(
                int(CONFIG['Server']['UNBANNED_CHANNEL_ID']))
        self.streamer_name = CONFIG['Server']['STREAMER_NAME']
        self.client_id = CONFIG['Server']['CLIENT_ID']
        self.client_secret = CONFIG['Server']['CLIENT_SECRET']
        asyncio.create_task(self._checker())

    @commands.command(aliases = ['un','ban','banned','isbanned','u'])
    async def unbanned(self, ctx: commands.Context, arg = None):
        ''' Узнает разбанили ли ваню '''
        if arg:
            if await self._find_is_channel_unbanned(str(arg).lower()):
                await ctx.channel.send(f"{str(arg)} не в бане!")
            else:
                await ctx.channel.send(f"{str(arg)} аккаунта не существет, либо он в бане 😔")

            return 
        if await self._find_is_channel_unbanned(self.streamer_name):
            await ctx.channel.send("РАЗБАНИЛИИ 🥳🥳🥳🥳\nЗАХОДИИ https://www.twitch.tv/ehchobyah")
        else:
            await ctx.channel.send("Ваню не разбанили😔😭")

    async def _checker(self):
        while True:
            await asyncio.sleep(300)
            time_now = datetime.now().strftime("%d-%m-%Y %H:%M")
            if await self._find_is_channel_unbanned(self.streamer_name):
                await self.unbanned_channel.send(f"На момент {time_now}(мск) Ваню РАЗБАНИЛИИ🥳🥳🥳🥳\nЗАХОДИИ https://www.twitch.tv/ehchobyah") 
            else:
                await self.unbanned_channel.send(f"На момент {time_now}(мск) Ваня все еще в бане😞😔😭😭") 


    async def _find_is_channel_unbanned(self, streamer_name = None):
        if not streamer_name:
            streamer_name = self.streamer_name
        async with ClientSession() as session:
            data = {"client_id":self.client_id,
                   "client_secret":self.client_secret,
                   "grant_type":"client_credentials"}
            async with session.post('https://id.twitch.tv/oauth2/token',
                                params={'Content-Type':'application/x-www-form-urlencoded'},
                                data=data) as access:
                access_result = await access.json()
            async with session.get(f'https://api.twitch.tv/helix/users?login={streamer_name}',
                                   headers={'Authorization':'Bearer '+access_result['access_token'],
                                           'Client-Id':self.client_id}) as result:
                data = await result.json() 
                if data['data'] != []:
                    return True 
                else:
                    return False 

async def setup(bot: commands.Bot):
    await bot.add_cog(Unbanned(bot))
