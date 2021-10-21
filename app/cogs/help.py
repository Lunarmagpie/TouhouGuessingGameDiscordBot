import discord
from discord.ext import commands
from app.bot import Bot

class Help(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
    
    @commands.command()
    async def help(self,ctx,*args):
        embed = discord.Embed(
            title = "List of commands",
            color = 0xfcba03,
            description=f"Optional parameters are (in parentheses)."
        )
        embed.add_field(name="t.start", value="Start a guessing game.", inline="True")
        embed.add_field(name="t.stop", value="Stop a guessing game (does not work in challenge mode).", inline="True")
        embed.add_field(name="t.endless", value="Start an endless guessing game.", inline="True")
        embed.add_field(name="t.challenge @user", value="Play 5 guessing games against another player.", inline="True")
        embed.add_field(name="t.profile (@user)", value="Show a player's stats, or yours if not specified.", inline="True")
        embed.add_field(name="t.favorite character", value="Set your favorite character.", inline="True")
        embed.add_field(name="t.leaderboard", value="Show the global point leaderboard.", inline="True")
        embed.add_field(name="t.serverleaderboard", value="Show the server point leaderboard.", inline="True")
        embed.add_field(name="t.credits", value="Show the bot's credits & contact information.", inline="True")
        embed.add_field(name="t.vote", value="Vote for this bot on top.gg.", inline="True")
        embed.add_field(name="t.help", value="Show this menu.", inline="True")
        embed.add_field(name="** **", value="** **", inline="True")
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Help(bot))
