import discord
from discord.ext import commands
from app.bot import Bot
from app.util import scoreboard
from ..config import CHARACTER_DATBASE

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

        c = scoreboard.add_commas_to_number
        most_guessed = str.title(max(player_info['guessed_characters'], key=player_info['guessed_characters'].get))
        favorite = player_info.get('favorite')
        if (favorite == None): url = [x for x in CHARACTER_DATBASE if x['name'] == most_guessed][0]['image']
        else: url = [x for x in CHARACTER_DATBASE if x['name'] == favorite][0]['image']
        embed = discord.Embed(
            color = 0xfcba03,
            description=f'''\
            :medal: Total points acquired: **{c(player_info['score'])}**
            :grey_question: Total guesses: **{c(player_info['guesses'])}**
            :star: Total correct guesses: **{c(player_info['games_won'])}**
            :punch: Total challenges played: **{c(player_info['challenge_mode_games_played'])}**
            :trophy: Total challenges won: **{c(player_info['challange_mode_games_won'])}**
            :face_in_clouds: Most guessed character: **{most_guessed}**
            :yellow_heart: Favorite character: {"**" + favorite + "**" if favorite != None else "*Not set*"}
            '''
        )
        embed.set_author(name=f"{user.name}'s Profile", icon_url=user.avatar_url)
        embed.set_image(url=url)
        await ctx.channel.send(embed=embed)

def setup(bot: "Bot"):
    bot.add_cog(Profile(bot))
