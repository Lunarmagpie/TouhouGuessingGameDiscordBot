from app.util import characters
from app.config import CHARACTER_DATBASE

def main():
    for entry in CHARACTER_DATBASE:
        char_name = entry['name']
        jp_char_name = char_name.split(" ")
        if len(jp_char_name) == 2:
            jp_char_name.reverse()
            jp_char_name = " ".join(jp_char_name).lower()

            print(f"\"{jp_char_name}\" : \"{char_name}\",")

if __name__ == "__main__":
    main()