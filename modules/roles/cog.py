import random
from discord.ext import commands
from config import CONFIG


class Roles(commands.Cog, name="Roles module"):
    ''' Получи случайную роль на сервере '''

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.roles_channel = self.bot.get_channel(
            int(CONFIG['Server']['ROLE_CHANNEL_ID']))

    @commands.command()
    async def randomrole(self, ctx: commands.Context):
        '''Присваивает вам случайную роль '''
        if ctx.channel == self.roles_channel:
            await assign_random_role(ctx, ctx.author)

async def assign_random_role(ctx, member):
    """ Присваивает случайную роль участнику сервера """
    server = member.guild
    user_roles = [role for role in member.roles if not (
        role.permissions.administrator or role.name == '@everyone')]

    # Снимаем существующие роли с пользователя
    try:
        await member.remove_roles(*user_roles, reason='Снятие всех ролей перед присвоением новой роли')
    except:
        print(f'Не удалось удалить все роли у {member}')

    roles = [role for role in server.roles if not (
        role.permissions.administrator or role.name == '@everyone')]

    # Если роли есть, присваеваем случайно выбранную роль пользователю
    if roles:
        random_role = random.choice(roles)
        try:
            await member.add_roles(random_role)
            # Если удалось присвоить роль, уведомляем пользователя об этом
            try:
                await member.send(f'Поздравляю, вы получили роль: {random_role.name}')
            except:
                print(
                    f'Не удалось отправить сообщение о получении роли {member}')
            finally:
                await ctx.send(f'{ctx.author.mention}, ваша случайная роль: {random_role}')
        except:
            print(f'Не удалось присвоить роль пользователю {member}')


async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot))
