from pincer import Client
from pincer.objects import Embed, MessageContext
from app.util import scoreboard, command
from pymongo import CursorType


class Leaderboard:
    def __init__(self, bot: Client):
        self.bot = bot

    def get_leaderboard_embed(
        self,
        ctx: MessageContext,
        res: CursorType,
        title: str = "Global - Top 20 players",
        icon: str = "https://i.imgur.com/lO4WPig.png"
    ) -> Embed:
        out = ""

        for i, user in enumerate(res):
            # Can remove once its confirmed that all top 20 players have a username
            try:
                name = user['username']
            except KeyError:
                name = "None"

            if i == 0:
                place_medal = ":first_place:"
            elif i == 1:
                place_medal = ":second_place:"
            elif i == 2:
                place_medal = ":third_place:"
            else:
                place_medal = f"{i+1}."

            out += (
                f"{place_medal} **{name}** - {scoreboard.add_commas_to_number(user['score'])} points\n"  # noqa: E501
            )
            # if i == 2: out += "\n"

        embed = Embed(
            # title = "Top 20 Players",
            color=0xfcba03
        )
        embed.set_author(name=title, icon_url=icon)
        embed.add_field(name='​', value=out, inline=True)
        return embed

    @command(description="Show the global leaderboard.")
    async def leaderboard(self, ctx: MessageContext):
        # player_info = scoreboard.get_player_information(ctx.author)
        res = scoreboard.table.find().sort("score", -1).limit(20)
        return self.get_leaderboard_embed(ctx, res)

    @command(description="Show the leadboard for people who have played on this server.")
    async def serverleaderboard(self, ctx: MessageContext):
        # player_info = scoreboard.get_player_information(ctx.author)
        res = scoreboard.table.find(
            {"servers": ctx.guild_id}).sort("score", -1).limit(20)

        guild = self.bot.guilds[ctx.guild_id]
        title = f"{guild.name} - Top 20 players"
        if guild.icon:
            icon = f"https://cdn.discordapp.com/icons/{guild.id}/{guild.icon}.png"
        else:
            icon = "https://i.imgur.com/S7cZnUD.png"
        return self.get_leaderboard_embed(ctx, res, title, icon)


setup = Leaderboard
