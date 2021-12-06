from pincer.client import Client
from pincer.objects import User
from pincer.objects.message.context import MessageContext

from app.util import command
from app.classes.guessing_game import GuessingGame, guessing_game_channel_lock
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
    async def stop(self, ctx: MessageContext):
        if ctx.channel_id in guessing_game_channel_lock:
            guessing_game_channel_lock[ctx.channel_id].game_loop.cancel()
            await guessing_game_channel_lock[ctx.channel_id].send_game_ended_by_user_embed(ctx)
            del guessing_game_channel_lock[ctx.channel_id]
        else:
            await ctx.send("A guessing game isn't running in this channel!")

    # @command()
    # async def endless(self, ctx):
    #     g = EndlessGuessingGame(ctx.channel, self.bot, ctx.author)
    #     await g.start()

    # @command()
    # async def challenge(self, ctx, user: User):
    #     g = Challenge(ctx.channel, self.bot, ctx.author, user)
    #     await g.start()


setup = Guess
