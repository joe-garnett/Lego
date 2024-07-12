import os
import numpy as np
import json
from PIL import Image
from math import sqrt

def get_image(filename):
    path = os.path.join('images', (filename + '.jpg'))

    if os.path.exists:
        return path
    else:
        print("Image not found")
        return -1
    
img = Image.open(get_image("image8"))

print(img.width)
print(img.height)