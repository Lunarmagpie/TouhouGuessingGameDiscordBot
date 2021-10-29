import discord
from discord.ext import commands
from app.bot import Bot
from app.util import characters
from ..config import CHARACTER_DATBASE

class View_character(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command(aliases=['c', 'info'])
    async def character(self,ctx,*arg: str):
        name = " ".join(arg)
        nameLower = name.lower()
        for index in CHARACTER_DATBASE:
            if nameLower == index["name"].lower():
                        char_name = name.title().replace("No", "no")
                        char = characters.get_character(char_name)
                        url = [x for x in CHARACTER_DATBASE if x['name'] == char_name][0]['image']
                        embed = discord.Embed(
                            color = 0xfcba03,
                            title = char_name,
                            description=f'''\
                            :grey_question: Guess Rate: **{100 if char["total_guesses"] == 0 else int(
                                char["total_correct_guesses"] / char["total_guesses"] * 100)}%**
                            :yellow_heart: Favorites: **{char["total_favorites"]}**
                            '''
                        )
                        embed.set_image(url=url)
                        await ctx.channel.send(embed=embed)
                        return
        await ctx.channel.send(f'**"{name}"** is not a valid character!')
        return

def setup(bot: "Bot"):
    bot.add_cog(View_character(bot))