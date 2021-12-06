from pincer import Client
from pincer.objects import Embed
from pincer.commands import CommandArg, Description

from app.util import characters, command
from app.nicknames import nicknames
from ..config import CHARACTER_DATBASE


class ViewCharacterCog:
    def __init__(self, bot: Client):
        self.bot = bot

    @command(description="View a character")
    async def character(self, name: CommandArg[
        str,
        Description["Character name"]  # type: ignore # noqa: F722
    ]):
        name = name.lower()
        name = nicknames.get(name, name).lower()

        for index in CHARACTER_DATBASE:
            if name == index["name"].lower():
                char_name = name.title().replace("No", "no")
                char = characters.get_character(char_name)
                url = [x for x in CHARACTER_DATBASE if x['name']
                       == char_name][0]['image']
                embed = Embed(
                    color=0xfcba03,
                    title=char_name,
                    description=f'''\
                            :grey_question: Guess Rate: **{100 if char["total_guesses"] == 0 else
                            int(char["total_correct_guesses"] / char["total_guesses"] * 100)}%**
                            :yellow_heart: Favorites: **{char["total_favorites"]}**
                            '''
                )
                embed.set_image(url=url)
                return embed

        return f'**"{name}"** is not a valid character!'


setup = ViewCharacterCog
