from app.config import CHARACTER_DATBASE
from PIL import Image
import PIL
import numpy as np
import requests


def create_silhouette(img, name):
    image = Image.open(requests.get(img, stream=True).raw)

    x = np.array(image)
    r, g, b, a = np.rollaxis(x, axis=-1)
    r[a!=0] = 0
    g[a!=0] = 0
    b[a!=0] = 0
    x = np.dstack([r, g, b, a])
    image = Image.fromarray(x, 'RGBA')
    image.save(f"data/silhouettes/{name}.png", 'PNG')

for char in CHARACTER_DATBASE:
    create_silhouette(char['image'], char['name'])
