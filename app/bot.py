from pincer import Client

from glob import glob
import time
import os


class Bot(Client):
    def __init__(self, *args, **kwargs) -> None:
        self.load_cogs()
        super().__init__(*args, **kwargs)

        # self.dbl_token = os.environ["thdbltoken"]
        self.dbl_token = None
        # self.topggpy = topgg.DBLClient(self, self.dbl_token)

    def load_cogs(self):
        """Load all cogs from the `cogs` directory."""
        for cog in glob("app/pincer_cogs/*.py"):
            self.load_cog(cog.replace("/", ".").replace("\\", ".")[:-3])

    def run(self):
        print("Touhou Bot!")
        return super().run()

    @Client.event
    async def on_ready(self):
        print(f"Logged in after {time.perf_counter():,.3f}s")
