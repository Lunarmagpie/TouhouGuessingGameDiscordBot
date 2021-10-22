import discord
from discord.ext import tasks, commands
from app.bot import Bot
from app.util import scoreboard
from ..config import CHARACTER_DATBASE

class Manage_Data(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.remove_old_data.start()

    @tasks.loop(hours=12)
    async def remove_old_data(self):
        try:
            scoreboard.return_old_data(self.bot)
        except Exception as e:
            print(e)

def setup(bot: "Bot"):
    bot.add_cog(Manage_Data(bot))