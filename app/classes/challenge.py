from ..config import CHARACTER_DATBASE
from .guessing_game import GuessingGame
import random
import discord
import time
import math
import asyncio

class Challenge(GuessingGame):
    def __init__(self, channel, bot, author, *args):
        super().__init__(channel, bot, author)
        self.args = args

    async def challenge(self):
        print(self.args)
        if self.args == None:
            await self.channel.send("You must mention a player to challenge!")
            return
        await self.start(opponent=1738452398452378945)
