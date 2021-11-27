from app.config import CHARACTER_DATBASE
from app.util import hash_character_name
from PIL import Image
import PIL
import numpy as np
import requests
import math


def create_silhouette(img, name):
    image = Image.open(f"data/images/{name}.png")

    x = np.array(image)
    r, g, b, a = np.rollaxis(x, axis=-1)
    r.fill(0)
    g.fill(0)
    b.fill(0)
    x = np.dstack([r, g, b, a])

    image = Image.fromarray(x, 'RGBA')
    name = hash_character_name(name)
    image.save(f"data/silhouettes/{name}.png", 'PNG')

def center(img, name):
    image = Image.open(f"data/images/{name}.png")

    color = (0, 0, 0, 0)
    width, height = image.size
    new_width = math.floor(height * 1.03)
    new_height = height

    left = math.floor((new_width - width) / 2)
    top = 0

    result = Image.new(image.mode, (new_width, new_height), color)
    result.paste(image, (left, top))

    result.save(f"data/images/{name}.png", 'PNG')
    return result

def fix_specific_character(name):
    for i,char in enumerate(CHARACTER_DATBASE):
        if name == char['name']:
            center(char['image'], char['name'])
            create_silhouette(char['image'], char['name'])
            print(f"{i} - {char}")

def main():
    fix_specific_character("Yuuma Toutetsu")

if __name__ == "__main__":
    main()
