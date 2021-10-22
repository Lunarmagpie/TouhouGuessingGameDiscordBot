import discord
from discord.ext import commands,tasks
from app.util import scoreboard
import topgg

import time
import os
from . import config

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("t.", ),help_command=None
        )

        for filename in os.listdir(os.path.join("app", "cogs")):
            if filename.endswith("py"):
                self.load_extension(f"app.cogs.{filename[:-3]}")

        self.dbl_token = os.environ["thdbltoken"]
        self.topggpy = topgg.DBLClient(self, self.dbl_token)

    def run(self):
        print("Touhou Bot!")
        return super().run(os.environ["thtoken"])


    async def process_commands(self, message):
        for cmd in self.command_prefix(self, message):
            if message.content.startswith(cmd):
                scoreboard.time_last_updated(message.author)
                break

        return await super().process_commands(message)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.guild:
            return

        try:
            await self.process_commands(message)
        except Exception as e:
            print(e)

    async def on_connect(self):
        print(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")
