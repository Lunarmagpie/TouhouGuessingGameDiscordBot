import discord
from discord.ext import commands
from app.bot import Bot
from app.util import scoreboard
import asyncio

class Leaderboard(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def leaderboard(self,ctx,*args):
        # player_info = scoreboard.get_player_information(ctx.author)
        res = scoreboard.table.find().sort("score",-1).limit(20)

        out = ""

        for i,user in enumerate(res):
            #Can remove once its confirmed that all top 20 players have a username
            try:
                name = user['username']
            except:
                name = "None"

            place_medal = f"{i+1}."
            if i == 0: place_medal = ":first_place:"
            if i == 1: place_medal = ":second_place:"
            if i == 2: place_medal = ":third_place:"

            out += (f"{place_medal} **{name}** - {user['score']} points\n")
            if i == 2: out += "\n"

        embed = discord.Embed(
            title = "Top 20 Players",
            color = 0xfcba03
        )
        embed.add_field(name='​', value=out, inline=True)
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Leaderboard(bot))
