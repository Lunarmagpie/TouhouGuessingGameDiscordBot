from discord.ext import commands
from app.bot import Bot

class TemplateCog(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot


def setup(bot: "Bot"):
    bot.add_cog(TemplateCog(bot))