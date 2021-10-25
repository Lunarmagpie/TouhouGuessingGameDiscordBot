from app.util import scoreboard
from app.util import characters
from app.config import CHARACTER_DATBASE

def main():
    char_list = []
    for user in scoreboard.get_every_player():
        print(user)
        try:
            favorite = user["favorite"]
            if favorite != "":
                characters.update_favorites(favorite, False)
                
        except(KeyError):
            pass

if __name__ == "__main__":
    main()