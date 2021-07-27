from discord.ext import commands
from app.bot import Bot

class TemplateCog(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def hello(self,ctx):
        await ctx.channel.send("Hello world!")


def setup(bot: "Bot"):
    bot.add_cog(TemplateCog(bot))