from discord.ext import commands
from app.bot import Bot
from app.classes.guessing_game import GuessingGame

class TemplateCog(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

def setup(bot: "Bot"):
    bot.add_cog(TemplateCog(bot))
