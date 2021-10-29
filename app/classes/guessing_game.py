from ..config import CHARACTER_DATBASE
from app.util import scoreboard
from app.util import characters
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
        embed.set_footer(text="Type 't.stop' to stop the game!")
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

        # Update number of games played for the character
        characters.update_times_appeared(self.char['name'])


        await self.channel.send(embed=embed)

    async def send_game_ended_by_user_embed(self):
        embed = discord.Embed(title=f"The game was ended!", color = 0x3B88C3, description=f"The character is **{self.char['name']}**.")
        embed.set_image(url=self.char["image"])

        # Update number of games played for the character
        characters.update_times_appeared(self.char['name'])

        await self.channel.send(embed=embed)

    async def send_game_already_running(self):
        await self.channel.send("Game already running!")

    def update_score(self, guild, author, points):
        scoreboard.update_attr(author, "guesses", 1)
        scoreboard.update_attr(author, "score", points)
        scoreboard.update_attr(author, "games_won", 1)
        scoreboard.update_character_guessed_count(author,self.char_name)
        scoreboard.update_serverlist(author, guild)

        # Update character correct guesses
        characters.update_correct_guesses(self.char['name'])
        characters.update_times_appeared(self.char['name'])

    def end_game(self):
        try:
            del guessing_game_channel_lock[self.channel.id]
        except KeyError:
            pass

    async def timeout(self):
        await self.send_timeout_embed()
        self.end_game()

    def check_guess(self, msg):
        if msg.channel == self.channel and not msg.author.bot:
            if msg.content == "t.stop" and self.can_stop_game:
                asyncio.create_task(self.send_game_ended_by_user_embed())
                self.end_game()
                return True
            elif msg.content.startswith("t."):
                pass
            elif msg.content.lower() == self.char["name"].lower() or msg.content.lower() == self.jp_char_name.lower():
                self.end_time = time.time()
                self.points = math.floor(max(1, 10 - (self.end_time - self.start_time))) * 2 + (self.attempts - 1) * 3
                self.winners.append(msg.author)
                asyncio.create_task(self.send_correct_guess_embed(msg))
                self.end_game()

                #add score to database
                self.update_score(msg.guild.id, msg.author, self.points)
                scoreboard.update_username(msg.author)
                scoreboard.update_serverlist(msg.author, msg.guild.id)

                return True
            else:
                scoreboard.update_attr(msg.author, "guesses", 1)
                scoreboard.update_username(msg.author)
                scoreboard.update_serverlist(msg.author, msg.guild.id)
                characters.update_guesses(self.char_name)
                # No warning to avoid rate limiting
                # asyncio.create_task(self.send_incorrect_guess_warning_embed())
                asyncio.create_task(msg.add_reaction("❌"))
                return False
        else:
            return False

    async def game_loop(self,custom_title):
        self.randomize_character()
        self.start_time = time.time()
        await self.send_question_embed(custom_title)

        try:
            message = await self.bot.wait_for('message', check=self.check_guess, timeout = 20)
        except asyncio.TimeoutError:
            await self.timeout()
        await asyncio.sleep(0.3)

    async def start(self, custom_title="Who's that 2hu?") -> None:
        if self.channel.id in guessing_game_channel_lock:
            await self.send_game_already_running()
            return
        else:
            guessing_game_channel_lock[self.channel.id] = True

        await self.game_loop(custom_title)
        