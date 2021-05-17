from pathlib import Path
from urllib.request import urlopen

import colorgram
from PIL import Image
from tqdm import tqdm
import pandas as pd

# all punks

url = "https://raw.githubusercontent.com/larvalabs/cryptopunks/master/punks.png"
img = Image.open(urlopen(url))

# check

img.height
img.width
img.crop((0, 0, 24, 24))

# crop

for y in range(0, 100):
    for x in range(0, 100):
        id =  x + (y * 100)
        left = x * 24
        upper = y * 24
        right = (x + 1) * 24
        lower = (y + 1) * 24
        box = (left, upper, right, lower)
        punk = img.crop(box)
        punk.save(f"png/{id}.png")
