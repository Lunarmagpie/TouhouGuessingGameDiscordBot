import discord
from discord.ext import commands
from app.bot import Bot
from app.util import scoreboard
from app.classes.scoreboard import UserNotFoundError

class Profile(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def profile(self,ctx,*args):
        try:
            player_info = scoreboard.get_player_information(ctx.author)
        except UserNotFoundError:
            player_info = {
                "score" : 0,
                "games_won" : 0,
            }
        embed = discord.Embed(
            color = 0xfcba03,
            description=f"Total points acquired: **{player_info['score']}**\nTotal questions answered: **{player_info['games_won']}**"
        )
        embed.set_author(name=f"{ctx.author.name}'s Statistics", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Profile(bot))
