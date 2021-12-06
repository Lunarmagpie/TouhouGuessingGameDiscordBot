import asyncio
import discord
from discord.ext import tasks, commands
from app.bot import Bot
from app.util import scoreboard
from ..config import CHARACTER_DATBASE

class Manage_Data(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.bot.manage_data = self

    @tasks.loop(hours=6)
    async def remove_old_data(self):
        print("Attempting to remove old data...")
        try:
            scoreboard.return_old_data(self.bot)
        except Exception as e:
            print(e)

    async def call_remove_old_data(self):
        await asyncio.sleep(100)
        self.remove_old_data.start()

def setup(bot: "Bot"):
    bot.add_cog(Manage_Data(bot))