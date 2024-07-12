import os
import json
from PIL import Image
from math import sqrt

"""
A rather naive but fairly functional solution to 'legoifying' an image
Next steps, perhaps for a v2 when I have improved:
- A more informed approach, e.g detecting objects, edges, colors of interest for the pixelation algo
- Provide instructions for assembly
- More user friendly
"""
# Retrieve Image From File
def get_image(filename):
    path = os.path.join('images', (filename + '.jpg'))
    if os.path.exists:
        return path
    else:
        print("Image not found")
        return -1

# Retrieve json data
def retrieve_colors():
    # data is not ALL lego colors, just those that can be bought easily
    path = os.path.join('data', 'colors.json')
    with open(path) as f:
        return json.load(f)
         
# Finds color that is most similar to the possible lego colors
def find_closest_color(r, g, b, rgb_colors):
    min_distance = float('inf')
    closest_color = None
    # Just 3d pythagoras (rgb is a cube)
    for color, (rc, gc, bc) in rgb_colors.items():
        distance = sqrt((r - rc)**2 + (g - gc)**2 + (b - bc)**2) 
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color

# Goes through every pixel in (scaled) image and updates the pixel according to its closes lego color
def update_pixels(pixels, width, height, rgb_colors):
    colors_count = {}
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            closest_color = find_closest_color(r, g, b, rgb_colors)
            pixels[x, y] = tuple(rgb_colors[closest_color])
            if closest_color in colors_count:
                colors_count[closest_color] += 1
            else:
                colors_count[closest_color] = 1
    return colors_count

# Reduces number of colors until number of studs is >= threshold
# (because 1 stud of say 'Dark-Purple' is really incovenient to buy)
def filter_colors(rgb_colors, colors_count, threshold=50):
    for c in list(colors_count):
        if colors_count[c] < threshold and c in rgb_colors:
            del rgb_colors[c]

def avg_colors(path, width, height):
    # Loads image, scales it, and 'pixelates' it using nearest neighbour
    img = Image.open(path)
    pixelated_img = img.resize((width, height), Image.NEAREST)
    pixelated_img = pixelated_img.convert('RGB')
    pixels = pixelated_img.load()
    rgb_colors = retrieve_colors()

    # Repeats filter process untill all colors have >= threshold studs
    # I'd imagine there's a much more efficient way of doing this, for my purposes at this resolution a faster way it not needed
    while True:
        colors_count = update_pixels(pixels, width, height, rgb_colors)
        filter_colors(rgb_colors, colors_count)
        if all(count >= 50 for count in colors_count.values()):
            break

    # Console output, and a picture of the pixelated image
    print(dict(sorted(colors_count.items(), key=lambda item: item[1])))
    total = sum(colors_count.values())
    print(f'Total studs: {total}')
    print(f'Estimated Price: {total * 0.03}')
    pixelated_img.save('pixelated_img.jpg')
    pixelated_large_img = pixelated_img.resize((img.width, img.height), Image.NEAREST)
    pixelated_large_img.show()

# Example usage
path = get_image("image9")
avg_colors(path, 64, 48)