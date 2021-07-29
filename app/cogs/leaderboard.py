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

        out_name = ""
        out_score = ""
        for player in res:
            user = await self.bot.fetch_user(player["player_id"])

            out_name += (f"**{user.name}**\t\n")
            out_score += (f"{player['score']} points\n")

        embed = discord.Embed(
            title = "Top 25 Players",
            color = 0xfcba03
        )
        embed.add_field(name='​', value=out_name, inline=True)
        embed.add_field(name='​', value=out_score, inline=True)
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Leaderboard(bot))
