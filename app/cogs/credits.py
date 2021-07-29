import discord
from discord.ext import commands
from app.bot import Bot
from app.util import scoreboard

class Credits(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def credits(self,ctx,*args):
        player_info = scoreboard.get_player_information(ctx.author)

        res = scoreboard.table.find().sort("score",-1).limit(25)

        out = ""
        for player in res:
            user = await self.bot.fetch_user(player["player_id"])

            out += (f"{user.name}: {player['score']}\n")
        
        embed = discord.Embed(
            title = "Credits",
            color = 0xfcba03,
            description=f"""
            💮 **Artists**:
                dairi: https://www.pixiv.net/en/users/4920496\nkaoru: https://www.pixiv.net/en/users/743845
            💮 **Development**:
                <@!318039587412901890>
                <@!318076068290494466>
            """
        )
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Credits(bot))
