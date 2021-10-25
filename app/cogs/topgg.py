import discord
from discord.ext import tasks,commands
from app.bot import Bot
import requests
from requests.api import head
import topgg

class Topgg(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        # self.update_stats.start()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        try:
            await self.bot.topggpy.post_guild_count()
            print(f"Posted server count ({self.bot.topggpy.guild_count})")
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")
    
    @commands.command()
    async def vote(self,ctx,*args):
        header = {"Authorization" : self.bot.dbl_token}
        res = requests.get(f"https://top.gg/api/bots/869410048743473182/check?userId={ctx.author.id}",headers=header)
        if res.status_code == 200:
            pass
        else:
            print(res.status_code)
            print(res.json())
            print(self.bot.dbl_token)
            raise Exception
        has_voted = True if res.json()["voted"] >= 1 else False

        has_voted_text = ""
        if has_voted: has_voted_text = "**You have already voted today!**"
        else: has_voted_text = "**You can currently vote!**"
        await ctx.channel.send(f"Please vote for Touhou Guesser! There are currently no rewards, but voting helps Touhou Guesser have more visibility.\nhttps://top.gg/bot/869410048743473182/vote\n\n{has_voted_text}")


def setup(bot: "Bot"):
    bot.add_cog(Topgg(bot))
