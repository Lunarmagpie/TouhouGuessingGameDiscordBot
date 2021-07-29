from typing import AsyncContextManager
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

        self.bot = bot
        self.author = author

        self.points = 0
        self.attempts = 3
        self.winners = []
        self.opponent = None
        self.can_stop_game = True
        self.game_running = False
    
    def check_guess(self,message):
        return message.channel == self.channel and not message.author.bot

    def randomize_character(self):
        self.character_index = random.choice(range(len(CHARACTER_DATBASE)))
        self.char = CHARACTER_DATBASE[self.character_index]
        self.char_name = self.char["name"]

        if len(self.char_name.split(" ")) == 2:
            self.jp_char_name = self.char_name.split(" ")
            self.jp_char_name.reverse()
            self.jp_char_name = " ".join(self.jp_char_name)
        else:
            self.jp_char_name = self.char_name

    async def send_question_embed(self, title):
        embed = discord.Embed(title=title, color = 0x3B88C3, description="Guess by typing the character's name in chat.")
        embed.set_image(url=self.char["silhouette"])
        embed.set_footer(text="Type `t.stop` to stop the game!")
        await self.channel.send(embed=embed)

    async def send_correct_guess_embed(self, msg):
        embed = discord.Embed(title=f"Correct!", color = 0x78B159, description=f"The character is **{self.char['name']}**.\n {msg.author.mention} has gained {self.points} point{'s' if self.points != 1 else ''}.")
        embed.set_image(url=self.char["image"])
        await self.channel.send(embed=embed)

    async def send_incorrect_guess_warning_embed(self):
        #embed = discord.Embed(title=f" Incorrect! {self.attempts} Attempt{'s' if self.attempts != 1 else ''} remaining.", color = 0xDD2E44)
        await self.channel.send("**Incorrect!**")

    async def send_timeout_embed(self):
        embed = discord.Embed(title=f"Time's up!", color = 0xDD2E44, description=f"The character is **{self.char['name']}**.")
        embed.set_image(url=self.char["image"])
        await self.channel.send(embed=embed)

    async def send_game_ended_by_user_embed(self):
        embed = discord.Embed(title=f"The game was ended!", color = 0x3B88C3, description=f"The character is **{self.char['name']}**.")
        embed.set_image(url=self.char["image"])
        await self.channel.send(embed=embed)

    def end_game(self):
        try:
            del guessing_game_channel_lock[self.channel.id]
        except KeyError:
            pass

    async def timeout(self):
        if self.game_running:
            await self.send_timeout_embed()
            self.end_game()

    async def process_guess(self,msg):
        self.end_time = time.time()

        if msg.content == "t.stop" and self.can_stop_game:
            await self.send_game_ended_by_user_embed()
            self.game_running = False
            self.end_game()
            return True
        elif msg.content.startswith("t."):
            pass
        elif msg.content.lower() == self.char["name"].lower() or msg.content.lower() == self.jp_char_name.lower():
            self.points = math.floor(max(1, 10 - (self.end_time - self.start_time))) * 2 + (self.attempts - 1) * 3
            self.game_running = False
            self.end_game()
            self.winners.append(msg.author)
            await self.send_correct_guess_embed(msg)

            #add score to database
            scoreboard.update_attr(msg.author, "guesses", 1)
            scoreboard.update_attr(msg.author, "score", self.points)
            scoreboard.update_attr(msg.author, "games_won", 1)
            scoreboard.update_character_guessed_count(msg.author,self.char["name"].lower())
            return True
        else:
            scoreboard.update_attr(msg.author, "guesses", 1)
            await self.send_incorrect_guess_warning_embed()
            return False

    async def game_loop(self,custom_title):
        self.randomize_character()
        self.start_time = time.time()
        await self.send_question_embed(custom_title)
        await asyncio.sleep(20)
        await self.timeout()

    async def start(self, custom_title="Who's that 2hu?") -> None:
        self.game_running = True
        guessing_game_channel_lock[self.channel.id] = self

        await self.game_loop(custom_title)
