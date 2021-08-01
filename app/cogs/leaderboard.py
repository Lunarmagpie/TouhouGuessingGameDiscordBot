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
        res = scoreboard.table.find().sort("score",-1).limit(25)

        out_name = ""
        out_score = ""

        for user in res:
            #Can remove once its confirmed that all top 20 players have a username
            try:
                name = user['username']
            except:
                name = "None"

            out_name += (f"**{name}**\t\n")
            out_score += (f"{user['score']} points\n")

        embed = discord.Embed(
            title = "Top 25 Players",
            color = 0xfcba03
        )
        embed.add_field(name='​', value=out_name, inline=True)
        embed.add_field(name='​', value=out_score, inline=True)
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Leaderboard(bot))
