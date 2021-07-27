from ..config import CHARACTER_DATBASE
import random
import discord

class GuessingGame:
    def __init__(self, channel) -> None:
        self.channel = channel
        self.character_index = random.choice(range(len(CHARACTER_DATBASE)))

    async def start(self) -> None:
        embed = discord.Embed(title="Guess")
        embed.set_image(url=CHARACTER_DATBASE[self.character_index]["image"])

        await self.channel.send(embed=embed)
