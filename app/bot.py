import discord
from discord.ext import commands
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
        return super().run(os.environ["token"])


    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.guild:
            return

        try:
            await self.process_commands(message)
        except Exception:
            pass

    async def on_connect(self):
        print(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")
