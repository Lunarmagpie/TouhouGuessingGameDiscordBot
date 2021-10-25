import discord
from discord.ext import commands
from app.bot import Bot
from app.util import scoreboard

class Credits(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def credits(self,ctx,*args):
        embed = discord.Embed(
            # title = "💮 Credits",
            color = 0xfcba03,
            description=""
        )
        embed.add_field(name="Artists", value=
            """
            dairi: https://www.pixiv.net/en/users/4920496
            kaoru: https://www.pixiv.net/en/users/743845
            baba: https://www.pixiv.net/en/users/3422465
            """, 
        inline = False)
        embed.add_field(name="Development", value=
            """
            <@!318039587412901890>
            <@!318076068290494466>
                    
            Please contact either of us if you have any questions, or want to request removal of your data. We'll try to respond as soon as possible!
            """, 
        inline = False)
        embed.add_field(name="Source", value=
            """
            If you want to view the source code or contribute to the project, it is available at https://github.com/Lunarmagpie/TouhouGuessingGameDiscordBot
            """, 
        inline = False)
        embed.set_author(name="Credits", icon_url="https://b.catgirlsare.sexy/GmYW8Bs86OFs.png")
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Credits(bot))
