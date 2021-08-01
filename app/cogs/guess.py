from requests.api import head
import discord
import requests
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
    async def endless(self,ctx):
        g = EndlessGuessingGame(ctx.channel, self.bot, ctx.author)
        await g.start()

    @commands.command()
    async def challenge(self,ctx,user: discord.User=None):
        g = Challenge(ctx.channel, self.bot, ctx.author, user)
        await g.start()

    # @commands.command()
    # async def serverleaderboard(self,ctx,*args):
    #     g = GuessingGame(ctx.channel, self.bot, ctx.author)
    #     await g.start()

    @commands.command()
    async def vote(self,ctx,*args):
        header = {"Authorization" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg2OTQxMDA0ODc0MzQ3MzE4MiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjI3ODQ4NjA5fQ.d8m28fK6NOo1dXbm4nrCLtgWcAmZKhgZOIdZv0H3yaQ"}
        res = requests.get(f"https://top.gg/api/bots/869410048743473182/check?userId={ctx.author.id}",headers=header).json()
        has_voted = True if res["voted"] >= 1 else False

        print(has_voted)
        await ctx.channel.send(f"{has_voted}Please vote for Touhou Character Guesser! Voting helps Touhou Character Guesser have more visibility.\nhttps://top.gg/bot/869410048743473182/vote")

    @commands.command()
    async def help(self,ctx,*args):
        embed = discord.Embed(
            title = "List of commands",
            color = 0xfcba03,
            description=f"Optional parameters are (surrounded by parentheses)."
        )
        embed.add_field(name="t.start", value="Start a guessing game.", inline="True")
        embed.add_field(name="t.stop", value="Stop a guessing game (does not work in challenge mode).", inline="True")
        embed.add_field(name="t.endless", value="Start an endless guessing game.", inline="True")
        embed.add_field(name="t.challenge (@user)", value="Play 5 guessing games against another player.", inline="True")
        embed.add_field(name="t.profile (@user)", value="Show a player's stats, or yours if not specified.", inline="True")
        embed.add_field(name="t.leaderboard", value="Show the global point leaderboard.", inline="True")
        embed.add_field(name="t.credits", value="Show the credits menu.", inline="True")
        embed.add_field(name="t.vote", value="Vote for this bot. No rewards are offered currently.", inline="True")
        # embed.add_field(name="t.serverleaderboard", value="Show the server point leaderboard.", inline="True")
        embed.add_field(name="t.help", value="Show this menu.", inline="True")
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Guess(bot))
