from pincer.client import Client
from pincer.objects import User
from pincer.objects.message.context import MessageContext

from app.util import command
from app.classes.guessing_game import GuessingGame
from app.classes.challenge import Challenge
from app.classes.endless import EndlessGuessingGame


class Guess:
    def __init__(self, bot: Client):
        self.bot = bot

    @command(description="Start a guessing game")
    async def start(self, ctx: MessageContext):
        channel = await self.bot.get_channel(ctx.channel_id)
        g = GuessingGame(ctx, channel, self.bot, ctx.author)
        await g.start()

    @command(description="Stop a guessing game.")
    async def stop():
        pass

    # @command()
    # async def endless(self, ctx):
    #     g = EndlessGuessingGame(ctx.channel, self.bot, ctx.author)
    #     await g.start()

    # @command()
    # async def challenge(self, ctx, user: User):
    #     g = Challenge(ctx.channel, self.bot, ctx.author, user)
    #     await g.start()


setup = Guess
