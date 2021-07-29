from ..config import CHARACTER_DATBASE
from app.util import scoreboard
import random
import discord
import time
import math
import asyncio

guessing_game_channel_lock = {}

class GuessingGame():
    def __init__(self, channel, bot, author) -> None:
        self.channel = channel

        self.character_index = random.choice(range(len(CHARACTER_DATBASE)))
        self.bot = bot
        self.author = author

        self.char = CHARACTER_DATBASE[self.character_index]
        self.char_name = self.char["name"]

        if len(self.char_name.split(" ")) == 2:
            self.jp_char_name = self.char_name.split(" ")
            self.jp_char_name.reverse()
            self.jp_char_name = " ".join(self.jp_char_name)
        else:
            self.jp_char_name = self.char_name

        self.points = 0
        self.attempts = 3
        self.winners = []
        self.opponent = None

        self.check_guess = lambda message: message.channel == self.channel and not message.author.bot

    def check_guess_oppponent(self, message):
        if self.opponent != None:
            return self.check_guess and (message.author.id == self.opponent.id or message.author == self.author)
        return self.check_guess

    async def send_question_embed(self, title):
        embed = discord.Embed(title=title, color = 0x3B88C3, description="Guess by typing the character's name in chat.")
        embed.set_image(url=self.char["silhouette"])
        await self.channel.send(embed=embed)

    async def send_correct_guess_embed(self, msg):
        embed = discord.Embed(title=f"Correct!", color = 0x78B159, description=f"The character is **{self.char['name']}**.\n {msg.author.mention} has gained {self.points} point{'s' if self.points != 1 else ''}.")
        embed.set_image(url=self.char["image"])
        await self.channel.send(embed=embed)

    async def send_incorrect_guess_warning_embed(self):
        #embed = discord.Embed(title=f"🛑 Incorrect! {self.attempts} Attempt{'s' if self.attempts != 1 else ''} remaining.", color = 0xDD2E44)
        embed = discord.Embed(title=f"🛑 Incorrect!", color = 0xDD2E44)
        await self.channel.send(embed=embed)

    async def send_incorrect_guess_embed(self):
        embed = discord.Embed(title=f"Time's up!", color = 0xDD2E44, description=f"The character is **{self.char['name']}**.")
        embed.set_image(url=self.char["image"])
        await self.channel.send(embed=embed)

    async def send_game_already_running(self):
        await self.channel.send("Game already running!")

    def end_game(self):
        del guessing_game_channel_lock[self.channel.id]

    async def start(self, opponent=None, custom_title="Who's that 2hu?") -> None:
        if self.channel.id in guessing_game_channel_lock:
            await self.send_game_already_running()
            return
        else:
            guessing_game_channel_lock[self.channel.id] = True

        start = time.time()
        await self.send_question_embed(custom_title)

        while True:

            try:
                msg = await self.bot.wait_for('message', check=self.check_guess_oppponent, timeout = 20 - (time.time() - start))
            except asyncio.TimeoutError:
                await self.send_incorrect_guess_embed()
                self.end_game()
                break

            end = time.time()

            if msg.content.lower() == self.char["name"].lower() or msg.content.lower() == self.jp_char_name.lower():
                self.points = math.floor(max(1, 10 - (end - start))) * 2 + (self.attempts - 1) * 3
                self.end_game()
                self.winners.append(msg.author)
                await self.send_correct_guess_embed(msg)

                #add score to database
                scoreboard.update_attr(msg.author, "score", self.points)
                scoreboard.update_character_guessed_count(msg.author,self.char["name"].lower())
                break

            # elif msg.content.lower() in self.char_name_array:
            #     self.points = math.floor(max(1, 10 - (end - start) - 3))
            #     self.end_game()
            #     await self.send_correct_guess_embed(msg)
            #     break

            # self.attempts -= 1

            # if self.attempts == 0:
            #     await self.send_incorrect_guess_embed()
            #     break

            await self.send_incorrect_guess_warning_embed()
