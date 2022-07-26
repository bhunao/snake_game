from random import randint

from pygame import Color


def change_color(segment_color):
    max_val = 57
    randr = randint(0, max_val)
    randb = randint(0, max_val)
    randg = randint(0, max_val)

    s = segment_color
    new_color = Color(s.r, s.g, s.b)
    print(new_color)
    new_color.r += randr if new_color.r + randr <= 255 else - new_color.r
    new_color.g += randg if new_color.g + randg <= 255 else - new_color.g
    new_color.b += randb if new_color.b + randb <= 255 else - new_color.b
    return new_color

