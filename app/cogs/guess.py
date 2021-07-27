from discord.ext import commands
from app.bot import Bot
from app.classes.guessing_game import GuessingGame

class Guess(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def start(self,ctx):
        g = GuessingGame(ctx.channel, self.bot, ctx.author)
        await g.start()

def setup(bot: "Bot"):
    bot.add_cog(Guess(bot))
