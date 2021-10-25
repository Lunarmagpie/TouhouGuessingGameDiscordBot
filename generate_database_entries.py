from app.util import characters
from app.config import CHARACTER_DATBASE

def main():
    for entry in CHARACTER_DATBASE:
        characters.create_entry(entry["name"])

if __name__ == "__main__":
    main()