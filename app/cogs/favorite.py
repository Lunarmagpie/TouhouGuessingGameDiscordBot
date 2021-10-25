import discord
from discord.ext import commands
from app.bot import Bot
from app.util import scoreboard
from app.util import characters
from ..config import CHARACTER_DATBASE

class Favorite(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
    
    @commands.command()
    async def favorite(self,ctx,*arg):
        arg1 = " ".join(arg)
        for index in CHARACTER_DATBASE:
            if arg1.lower() == index["name"].lower():
                characters.update_favorites(scoreboard.get_player_information(ctx.author)["favorite"], True)
                characters.update_favorites(index["name"], False)


                scoreboard.update_favorite_chracter(ctx.author, index["name"])
                await ctx.channel.send(f'Favorite character set to **{index["name"]}**')
                return
        await ctx.channel.send(f'**"{arg1}"** is not a valid character!')

def setup(bot: "Bot"):
    bot.add_cog(Favorite(bot))