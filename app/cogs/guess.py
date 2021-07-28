from discord.ext import commands
from app.bot import Bot
from app.classes.guessing_game import GuessingGame
from app.classes.challenge import Challenge

class Guess(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def start(self,ctx):
        g = GuessingGame(ctx.channel, self.bot, ctx.author)
        await g.start()

    @commands.command()
    async def challenge(self,ctx,*args):
        g = Challenge(ctx.channel, self.bot, ctx.author, *args)
        await g.challenge()

def setup(bot: "Bot"):
    bot.add_cog(Guess(bot))
