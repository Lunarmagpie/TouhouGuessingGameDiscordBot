from ..config import CHARACTER_DATBASE
from .guessing_game import GuessingGame
from collections import Counter
import random
import discord
import time
import math
import asyncio

class Challenge(GuessingGame):
    def __init__(self, channel, bot, author, *args):
        super().__init__(channel, bot, author)
        self.args = args

        self.check_is_opponent = lambda message: message.channel == self.channel and message.author.id == self.opponent

    async def start_full_game(self, title):
        await self.start(opponent=self.opponent, custom_title=title)
        self.character_index = random.choice(range(len(CHARACTER_DATBASE)))
        self.char = CHARACTER_DATBASE[self.character_index]

    async def challenge(self):
        print(self.args)
        if len(self.args) == 0:
            await self.channel.send("You must mention a player to challenge!")
            return

        self.opponent = int(self.args[0][3:-1])
        self.opponent_profile = await self.bot.fetch_user(self.opponent)
        await self.channel.send(f'<@!{self.opponent}>: Do you accept the challenge? Type "y" or "yes" to accept or anything else to decline.')

        msg = await self.bot.wait_for('message', check=self.check_is_opponent, timeout = 20)

        if msg.content == "y" or msg.content == "yes":
            print("true")
        else:
            await self.channel.send("Challenge declined.")
            return

        for i in range(1):
            await self.start_full_game(f"{self.author.name} vs {self.opponent_profile.name}: Round {i + 1} of 5")

        winner_list = Counter(self.winners).most_common(2)
        if len(winner_list) > 1:
            if winner_list[0][1] != winner_list[1][1]:
                winner = winner_list[0][0]
        if len(winner_list) == 1:
            winner = winner_list[0][0]
        else:
            while winner_list[0][1] == winner_list[1][1]:
                await self.channel.send(f"{self.author.name} vs {self.opponent_profile.name}: Extra round (Tiebreaker)")
                await self.start_full_game()
                winner_list = Counter(self.winners).most_common(2)

        winner = Counter(self.winners).most_common(1)[0][0]

        await self.channel.send(f'The winner is <@!{winner}>!\n<@!{winner}> has gained 50 points.')
