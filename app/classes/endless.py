from .guessing_game import GuessingGame, guessing_game_channel_lock
import discord
import time

class EndlessGuessingGame(GuessingGame):
    def __init__(self, channel, bot, author):
        super().__init__(channel, bot, author)
        self.continue_games = True
        self.response_recieved_during_game = False

    def end_game(self):
        if not self.response_recieved_during_game:
            self.continue_games = False
        return super().end_game()

    def check_guess(self, msg):
        if msg.content != "t.stop":
            #self.response_recieved_during_game = True
            pass
        return super().check_guess(msg)

    async def send_game_ended_by_user_embed(self):
        embed = discord.Embed(title=f"The game was ended!", color = 0x3B88C3, description=f"The character is **{self.char['name']}**.")
        embed.set_image(url=self.char["image"])
        if not self.response_recieved_during_game:
            embed.set_footer(text="Endless mode has ended!")
        await self.channel.send(embed=embed)

    async def send_timeout_embed(self):
        embed = discord.Embed(title=f"Time's up!", color = 0xDD2E44, description=f"The character is **{self.char['name']}**.")
        embed.set_image(url=self.char["image"])
        if not self.response_recieved_during_game:
            embed.set_footer(text="Endless mode has ended!")
        await self.channel.send(embed=embed)

    async def start(self, opponent=None, custom_title="Who's that 2hu?") -> None:
        if self.channel.id in guessing_game_channel_lock:
            await self.send_game_already_running()
            return
        else:
            guessing_game_channel_lock[self.channel.id] = True

        while self.continue_games == True:
            self.response_recieved_during_game = False
            await self.game_loop(custom_title)
