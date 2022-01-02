import random
import time
import math
import asyncio
from secrets import token_urlsafe

from pincer.commands import Button, ActionRow
from pincer.client import Client
from pincer.commands.components.button import ButtonStyle
from pincer.exceptions import TimeoutError
from pincer.objects import Embed
from pincer.objects.guild.channel import Channel
from pincer.objects.message.context import MessageContext
from pincer.objects.message.message import Message
from pincer.objects.user.user import User

from ..config import CHARACTER_DATBASE
from app.util import scoreboard
from app.util import characters
from app.nicknames import nicknames

guessing_game_channel_lock = {}


class GuessingGame():
    def __init__(self, cog, ctx: MessageContext, channel: Channel, bot: Client, author: User) -> None:
        self.ctx = ctx
        self.channel = channel

        self.cog = cog
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

    async def send_question_embed(self, title):
        embed = Embed(title=title, color=0x3B88C3,
                      description="Guess by typing the character's name in chat.")
        embed.set_image(url=self.char["silhouette"])

        await self.ctx.send(
            Message(
                embeds=[embed],
                components=[
                    ActionRow(
                        self.cog.end_game_button
                    )
                ]
            )
        )

    async def send_correct_guess_embed(self, msg):
        embed = Embed(title="Correct!", color=0x78B159,
                      description=f"The character is **{self.char['name']}**.\n {msg.author.mention} has gained {self.points} point{'s' if self.points != 1 else ''}.")
        embed.set_image(url=self.char["image"])
        await self.channel.send(embed)

    async def send_incorrect_guess_warning_embed(self):
        await self.channel.send("**Incorrect!**")

    async def send_timeout_embed(self):
        embed = Embed(title="Time's up!", color=0xDD2E44,
                      description=f"The character is **{self.char['name']}**.")
        embed.set_image(url=self.char["image"])

        # Update number of games played for the character
        characters.update_times_appeared(self.char['name'])

        await self.channel.send(embed)

    async def send_game_ended_by_user_embed(self, ctx: MessageContext):
        embed = Embed(title="The game was ended!", color=0x3B88C3,
                      description=f"The character is **{self.char['name']}**.")
        embed.set_image(url=self.char["image"])

        # Update number of games played for the character
        characters.update_times_appeared(self.char['name'])

        await ctx.send(embed)

    async def send_game_already_running(self):
        await self.ctx.send("Game already running!")

    def update_score(self, guild, author, points):
        scoreboard.update_attr(author, "guesses", 1)
        scoreboard.update_attr(author, "score", points)
        scoreboard.update_attr(author, "games_won", 1)
        scoreboard.update_character_guessed_count(author, self.char_name)
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
        if msg.channel_id == self.channel.id and not msg.author.bot:
            char_name = nicknames.get(msg.content.lower(), msg.content)

            if msg.content == "t.stop" and self.can_stop_game:
                asyncio.create_task(self.send_game_ended_by_user_embed())
                self.end_game()
                return True
            elif msg.content.startswith("t."):
                pass
            elif char_name.lower() == self.char["name"].lower():
                self.end_time = time.time()
                self.points = math.floor(
                    max(1, 10 - (self.end_time - self.start_time))) * 2 + (self.attempts - 1) * 3
                self.winners.append(msg.author)
                self.end_game()
                asyncio.create_task(self.update_database_win(msg))
                return True
            else:
                asyncio.create_task(self.update_database_loss(msg))
                return False
        else:
            return False

    async def update_database_win(self, msg):
        # add score to database
        self.update_score(msg.guild_id, msg.author, self.points)
        scoreboard.update_username(msg.author)
        scoreboard.update_serverlist(msg.author, msg.guild_id)

    async def update_database_loss(self, msg):
        scoreboard.update_attr(msg.author, "guesses", 1)
        scoreboard.update_username(msg.author)
        scoreboard.update_serverlist(msg.author, msg.guild_id)
        characters.update_guesses(self.char_name)

    async def game_loop(self, custom_title):
        self.randomize_character()
        self.start_time = time.time()
        await self.send_question_embed(custom_title)

        try:
            async for msg in self.bot.loop_for('on_message', loop_timeout=20):
                if self.check_guess(msg):
                    await self.send_correct_guess_embed(msg)
                    break
                else:
                    await msg.react("❌")

        except TimeoutError:
            await self.timeout()
        await asyncio.sleep(0.3)

    async def start(self, custom_title="Who's that 2hu?") -> None:
        if self.channel.id in guessing_game_channel_lock:
            await self.send_game_already_running()
            return
        else:
            guessing_game_channel_lock[self.channel.id] = self

        self.game_loop = asyncio.create_task(self.game_loop(custom_title))
        await self.game_loop

    async def end_game_button(self):
        print("here")
        self.end_game()
        return "Ended the guessing game"
