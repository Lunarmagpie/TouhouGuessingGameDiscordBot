import discord
from discord.ext import commands
from app.bot import Bot
from app.classes.guessing_game import GuessingGame
from app.classes.challenge import Challenge
from app.classes.endless import EndlessGuessingGame

class Guess(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def start(self,ctx):
        g = GuessingGame(ctx.channel, self.bot, ctx.author)
        await g.start()

    @commands.command()
    async def stop(self,ctx):
        pass

    @commands.command()
    async def endless(self,ctx):
        g = EndlessGuessingGame(ctx.channel, self.bot, ctx.author)
        await g.start()

    @commands.command()
    async def challenge(self,ctx,user: discord.User=None):
        g = Challenge(ctx.channel, self.bot, ctx.author, user)
        await g.start()

def setup(bot: "Bot"):
    bot.add_cog(Guess(bot))
