from ..config import CHARACTER_DATBASE
import random
import discord

class GuessingGame():
    def __init__(self, channel, bot, author) -> None:
        self.channel = channel
        self.character_index = random.choice(range(len(CHARACTER_DATBASE)))
        self.bot = bot
        self.author = author

        self.char = CHARACTER_DATBASE[self.character_index]

    async def start(self) -> None:
        embed = discord.Embed(title="Who's that 2hu?")
        embed.set_image(url=self.char["silhouette"])
        await self.channel.send(embed=embed)

        def check(m):
            return m.content.lower() == self.char["name"].lower() and m.channel == self.channel and m.author == self.author

        msg = await self.bot.wait_for('message', check=check)

        responseEmbed = discord.Embed(title=f"Correct!", description=f"The character is **{self.char['name']}**.\n {self.author.mention} has gained 1 point.")
        responseEmbed.set_image(url=self.char["image"])
        await self.channel.send(embed=responseEmbed)
