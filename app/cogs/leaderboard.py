import discord
from discord.ext import commands
from app.bot import Bot
from app.util import scoreboard

class Leaderboard(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def leaderboard(self,ctx,*args):
        player_info = scoreboard.get_player_information(ctx.author)

        res = scoreboard.table.find().sort("score",-1).limit(25)

        out = ""
        for player in res:
            user = await self.bot.fetch_user(player["player_id"])

            out += (f"{user.name}: {player['score']}\n")
        
        embed = discord.Embed(
            color = 0xfcba03,
            description=out
        )
        embed.set_author(name=f"Top 25 Players")
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Leaderboard(bot))
