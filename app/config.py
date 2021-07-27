import json
import os
import glob
from pathlib import Path
import urllib
from app.util import hash_character_name

CHARACTER_DATBASE = []
for filepath in glob.glob("data/images/*.png"):
    p = Path(filepath)
    filename = p.name
    char_name = filename.split(".")[0]
    img = f"https://raw.githubusercontent.com/Drakomire/TouhouGuessingGameDiscordBot/main/data/images/{urllib.parse.quote(char_name)}.png"
    s_img = f"https://raw.githubusercontent.com/Drakomire/TouhouGuessingGameDiscordBot/main/data/silhouettes/{urllib.parse.quote(hash_character_name(char_name))}.png"


    CHARACTER_DATBASE += [{
        "name" : char_name,
        "image" : img,
        "silhouette" : s_img
    }]
