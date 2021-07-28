import discord
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
    async def challenge(self,ctx,user: discord.User=None):
        g = Challenge(ctx.channel, self.bot, ctx.author, user)
        await g.challenge()

    @commands.command()
    async def leaderboard(self,ctx,*args):
        g = GuessingGame(ctx.channel, self.bot, ctx.author)
        await g.start()

    @commands.command()
    async def serverleaderboard(self,ctx,*args):
        g = GuessingGame(ctx.channel, self.bot, ctx.author)
        await g.start()




    @commands.command()
    async def help(self,ctx,*args):
        embed = discord.Embed(
            title = "List of commands",
            color = 0xfcba03,
            description=f"Optional parameters are (surrounded by parentheses)."
        )
        embed.add_field(name="t.start", value="Start a guessing game.", inline="True")
        embed.add_field(name="t.challenge (@user)", value="Play 5 guessing games against another player.", inline="True")
        embed.add_field(name="t.profile (@user)", value="Show a player's stats, or yours if not specified.", inline="True")
        embed.add_field(name="t.leaderboard", value="Show the global point leaderboard.", inline="True")
        embed.add_field(name="t.serverleaderboard", value="Show the server point leaderboard.", inline="True")
        embed.add_field(name="t.help", value="Show this menu.", inline="True")
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Guess(bot))
