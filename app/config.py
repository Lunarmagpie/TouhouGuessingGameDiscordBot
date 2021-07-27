import json
import os
import glob
from pathlib import Path
import urllib

CHARACTER_DATBASE = []
for filepath in glob.glob("data/images/*.png"):
    p = Path(filepath)
    filename = p.name
    char_name = filename.split(".")[0]
    img = f"https://raw.githubusercontent.com/Drakomire/TouhouGuessingGameDiscordBot/main/data/images/{urllib.parse.quote(filename)}"
    s_img = f"https://raw.githubusercontent.com/Drakomire/TouhouGuessingGameDiscordBot/main/data/silhouettes/{urllib.parse.quote(filename)}"


    CHARACTER_DATBASE += [{
        "name" : char_name,
        "image" : img,
        "silhouette" : s_img
    }]
