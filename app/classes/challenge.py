from ..config import CHARACTER_DATBASE
from .guessing_game import GuessingGame
from collections import Counter
from app.util import scoreboard
import random
import discord
import time
import math
import asyncio

DANCE_GIFS = [
    "https://media1.tenor.com/images/bb15b01585e46acca0bb8da48a9e915e/tenor.gif?itemid=21439783",
    "https://images-ext-2.discordapp.net/external/lnxRLGrr3G3ExzIPxewrbh4NsKYl14-dZS-eEETURNA/%3Fitemid%3D21415488/https/media1.tenor.com/images/a38d26ec396c9ae2421ec88fb9a6c646/tenor.gif",
    "https://images-ext-2.discordapp.net/external/rMGdb1CHcX3m_brrVwW0b3KPkxqfQy-NWSCIXah3jyY/%3Fitemid%3D5047801%2527/https/media1.tenor.com/images/990d7fe275aff54f8fc5f73881fb7ccc/tenor.gif",
    "https://images-ext-2.discordapp.net/external/pr78wExl9pNFCjMTJQQwSqBAtUWgBNzoKiibIS4nyk8/%3Fitemid%3D18209405/https/media1.tenor.com/images/6bc961d129cbb06859290a031b95f34f/tenor.gif", #Fumo
    "https://media1.tenor.com/images/397c2ea8b6a01b3c20112571df82056a/tenor.gif?itemid=13835198",
    "https://media1.tenor.com/images/a0c95eded5fbb4f78bcee8434d2a7338/tenor.gif?itemid=16765090",
    "https://thumbs.gfycat.com/WearyGreatGreathornedowl-max-1mb.gif",
    "https://moriyashrine.org/uploads/monthly_2018_09/2hu.gif.66e48f662f142d94cc6b03efee49bb14.gif",

]

class Challenge(GuessingGame):
    def __init__(self, channel, bot, author, user):
        super().__init__(channel, bot, author)
        self.opponent = user
        self.can_stop_game = False
        self.check_is_opponent = lambda message: message.channel == self.channel and message.author.id == self.opponent.id

    async def start_full_game(self, title):
        await super().start(opponent=self.opponent.id, custom_title=title)
        self.randomize_character()

    async def start(self):
        if self.opponent == None:
            await self.channel.send("You must mention a player to challenge!")
            return

        await self.channel.send(f'{self.opponent.mention}: Do you accept the challenge? Type "y" or "yes" to accept or anything else to decline.')

        msg = await self.bot.wait_for('message', check=self.check_is_opponent, timeout = 20)

        if msg.content == "y" or msg.content == "yes":
            scoreboard.update_attr(self.author,"challenge_mode_games_played",1)
            scoreboard.update_attr(self.opponent,"challenge_mode_games_played",1)

        else:
            await self.channel.send("Challenge declined.")
            return

        for i in range(1):
            await self.start_full_game(f"{self.author.name} vs {self.opponent.name}: Round {i + 1} of 5")

        winner_list = Counter(self.winners).most_common(2)
        if len(winner_list) > 1:
            if winner_list[0][1] != winner_list[1][1]:
                winner = winner_list[0][0]
        if len(winner_list) == 1:
            winner = winner_list[0][0]
        else:
            while True:
                if len(winner_list) == 0 or winner_list[0][1] == winner_list[1][1]:
                    await self.start_full_game(f"{self.author.name} vs {self.opponent.name}: Extra round (Tiebreaker)")
                else:
                    break
                winner_list = Counter(self.winners).most_common(2)

        winner = Counter(self.winners).most_common(1)[0][0]

        points = Counter(self.winners).most_common(1)[0][1] * 5 + 40

        embed = discord.Embed(
            title = f':crown: The winner is {winner.name}! :crown:',
            color = 0xfcba03,
            description=f'{winner.mention} has gained {points} points.'
        )
        embed.set_image(url=random.choice(DANCE_GIFS))
        await self.channel.send(embed=embed)


        scoreboard.update_attr(msg.author, "score", self.points)
        scoreboard.update_attr(winner,"challange_mode_games_won",1)
