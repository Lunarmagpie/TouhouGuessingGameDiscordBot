import discord
from discord.ext import commands
from app.bot import Bot
from app.util import scoreboard
import asyncio

class Leaderboard(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    async def send_leaderboard_embed(self,ctx,res,title="Global - Top 20 players",icon="https://i.imgur.com/lO4WPig.png"):
        out = ""

        for i,user in enumerate(res):
            #Can remove once its confirmed that all top 20 players have a username
            try:
                name = user['username']
            except:
                name = "None"

            if   i == 0: place_medal = ":first_place:"
            elif i == 1: place_medal = ":second_place:"
            elif i == 2: place_medal = ":third_place:"
            else: place_medal = f"{i+1}."

            out += (f"{place_medal} **{name}** - {scoreboard.add_commas_to_number(user['score'])} points\n")
            # if i == 2: out += "\n"

        embed = discord.Embed(
            # title = "Top 20 Players",
            color = 0xfcba03
        )
        embed.set_author(name=title, icon_url=icon)
        embed.add_field(name='​', value=out, inline=True)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def leaderboard(self,ctx,*args):
        # player_info = scoreboard.get_player_information(ctx.author)
        res = scoreboard.table.find().sort("score",-1).limit(20)
        await self.send_leaderboard_embed(ctx,res)

    @commands.command()
    async def serverleaderboard(self,ctx,*args):
        # player_info = scoreboard.get_player_information(ctx.author)
        res = scoreboard.table.find(
        { "servers": ctx.guild.id } ).sort("score",-1).limit(20)

        # for doc in res:
        #     print(doc)

        # return
        # print(res.explain())

        title = f"{ctx.guild.name} - Top 20 players"
        print(ctx.guild.icon_url)
        if len(ctx.guild.icon_url) > 0:
            icon = ctx.guild.icon_url
        else:
            icon = "https://i.imgur.com/S7cZnUD.png"
        await self.send_leaderboard_embed(ctx,res,title,icon)

def setup(bot: "Bot"):
    bot.add_cog(Leaderboard(bot))
