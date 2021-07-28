from .database import Database
import discord

class Player(Database):
    def __init__(self, channel, bot, author, *args) -> None:
        super().__init__("score", "score")

        self.channel = channel
        self.bot = bot
        self.author = author

    async def profile(self):
        dict = self.table.find_one({
            "player_id": 318039587412901890
        })

        embed = discord.Embed(
            color = 0xfcba03,
            description=f"Total points acquired: **{dict['score']}**\nTotal questions answered: **{dict['games_won']}**"
        )
        embed.set_author(name=f"{self.author.name}'s Statistics", icon_url=self.author.avatar_url)
        await self.channel.send(embed=embed)
