from pincer import Client
from pincer.objects import Embed, User, MessageContext
from pincer.commands import CommandArg, Description

from app.bot import Bot
from app.util import command, scoreboard
from ..config import CHARACTER_DATBASE


class Profile(Client):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @command(description="Get your profile or a user's profile")
    async def profile(
        self,
        ctx: MessageContext,
        user: CommandArg[
            User,
            Description["A user who's profile you want to see"]  # type: ignore # noqa: F722
        ] = None
    ):
        if user is None:
            user = ctx.author

        player_info = scoreboard.get_player_information(user)

        c = scoreboard.add_commas_to_number

        favorite = None
        if len(player_info['guessed_characters']) >= 1:
            most_guessed = str.title(
                max(player_info['guessed_characters'], key=player_info['guessed_characters'].get))
            favorite = player_info.get('favorite')
            if favorite is None:
                url = [x for x in CHARACTER_DATBASE if x['name']
                       == most_guessed][0]['image']
            else:
                url = [x for x in CHARACTER_DATBASE if x['name']
                       == favorite][0]['image']
        else:
            most_guessed = "N/A"
            url = ""

        embed = Embed(
            color=0xfcba03,
            description=f'''\
            :medal: Total points acquired: **{c(player_info['score'])}**
            :grey_question: Total guesses: **{c(player_info['guesses'])}**
            :star: Total correct guesses: **{c(player_info['games_won'])}**
            :punch: Total challenges played: **{c(player_info['challenge_mode_games_played'])}**
            :trophy: Total challenges won: **{c(player_info['challange_mode_games_won'])}**
            :face_in_clouds: Most guessed character: **{most_guessed}**
            :yellow_heart: Favorite character: {
                f"**{favorite}**" if favorite != None else "*Not set*"
            }
            '''
        )

        embed.set_author(name=f"{user.username}'s Profile", url=user.get_avatar_url())

        if url:
            embed.set_image(url=url)
        return embed


setup = Profile
