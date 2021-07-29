from .guessing_game import GuessingGame
import discord

class EndlessGuessingGame(GuessingGame):
    def __init__(self, channel, bot, author):
        super().__init__(channel, bot, author)
        self.continue_games = True
        self.response_recieved_during_game = False

    def end_game(self):
        if not self.response_recieved_during_game:
            self.continue_games = False
        return super().end_game()

    async def process_guess(self, msg):
        if msg != "t.stop":
            self.response_recieved_during_game = True
        return await super().process_guess(msg)

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

    async def start(self):
        while self.continue_games == True:
            self.randomize_character()
            self.response_recieved_during_game = False
            await super().start()
