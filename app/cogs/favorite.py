import discord
from discord.ext import commands
from app.bot import Bot
from app.util import scoreboard
from ..config import CHARACTER_DATBASE

class Favorite(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
    
    @commands.command()
    async def favorite(self,ctx,*arg):
        arg1 = " ".join(arg)
        for index in CHARACTER_DATBASE:
            if arg1.lower() == index["name"].lower():
                scoreboard.update_favorite_chracter(ctx.author, index["name"])
                await ctx.channel.send(f'Favorite character set to **{index["name"]}**')
                return
        await ctx.channel.send(f'**"{arg1}"** is not a valid character!')

def setup(bot: "Bot"):
    bot.add_cog(Favorite(bot))