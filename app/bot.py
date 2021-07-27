import discord
from discord.ext import commands

import time
import os

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__()

        for filename in os.listdir(os.path.join("app", "cogs")):
            if filename.endswith("py"):
                self.load_extension(f"app.cogs.{filename[:-3]}")

    def run(self):
        print("Touhou Bot!")
        return super().run(os.environ["token"])


    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if not message.guild:
            return

        if message.guild.id != self.config.mcoding_server_id:
            return

        await self.process_commands(message)

    async def on_connect(self):
        self.log(f"Logged in as {self.user} after {time.perf_counter():,.3f}s")