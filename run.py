from app.bot import Bot
import os

def main():
    #Entrypoint for bot
    global bot
    bot = Bot(os.environ["thtoken"])
    bot.run()

if __name__ == "__main__":
    main()
