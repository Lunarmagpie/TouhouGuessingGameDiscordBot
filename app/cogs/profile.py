import discord
from discord.ext import commands
from app.bot import Bot
from app.util import scoreboard

class Profile(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def profile(self,ctx,user=None):
        if user is None:
            user = ctx.author
            player_info = scoreboard.get_player_information(ctx.author)
        else:
            user = int(user[3:-1])
            user = await self.bot.fetch_user(user)
            player_info = scoreboard.get_player_information(user)

        embed = discord.Embed(
            color = 0xfcba03,
            description=f"Total points acquired: **{player_info['score']}**\nTotal questions answered: **{player_info['games_won']}**"
        )
        embed.set_author(name=f"{user.name}'s Statistics", icon_url=user.avatar_url)
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Profile(bot))
