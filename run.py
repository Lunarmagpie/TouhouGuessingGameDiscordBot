from pincer import Intents
from app.bot import Bot
import os


def main():
    # Entrypoint for bot
    global bot
    bot = Bot(os.environ["thtoken"], intents=Intents.GUILD_MESSAGES)
    bot.run()


if __name__ == "__main__":
    main()
