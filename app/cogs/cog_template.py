from discord.ext import commands
from app.bot import Bot
from app.classes.guessing_game import GuessingGame

class TemplateCog(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def start(self,ctx):
        g = GuessingGame(ctx.channel)
        await g.start()

def setup(bot: "Bot"):
    bot.add_cog(TemplateCog(bot))