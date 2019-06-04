import math
import random

def normalize_number(number, base):
    return number / base

def normalize_color(color_tuple):
    r, g, b, a = color_tuple
    return (normalize_number(r, 255), normalize_number(g, 255),
            normalize_number(b, 255), a)

def ease(max_number, tick, speed, negative=False):
    speed = speed / 1000
    sin_value = abs(math.sin(tick * speed)) if not negative else math.sin(
        tick * speed)
    return max_number * sin_value

def calc_coordinates_on_circle(degree, radius):
    radians = math.pi * degree / 180
    return (radius * math.sin(radians), radius * math.cos(radians))


def get_remaining_frame_time(time_elapsed, fps):
    frame_time_limit = 1.0 / fps
    time_remaining = frame_time_limit - time_elapsed
    return time_remaining if time_remaining > 0 else 0


def hue_to_rgb(t1, t2, hue):
    if hue < 0:
        hue += 6
    if hue >= 6:
        hue -= 6
    if hue < 1:
        return (t2 - t1) * hue + t1
    elif hue < 3:
        return t2
    elif hue < 4:
        return (t2 - t1) * (4 - hue) + t1
    else:
        return t1


def hsl_to_rgb(hue, sat, light):
    hue = hue / 60

    if light <= 0.5:
        t2 = light * (sat + 1)
    else:
        t2 = light + sat - (light * sat)

    t1 = light * 2 - t2
    r = hue_to_rgb(t1, t2, hue + 2) * 255
    g = hue_to_rgb(t1, t2, hue) * 255
    b = hue_to_rgb(t1, t2, hue - 2) * 255

    return (r, g, b)


def rgb_to_hsl(r, g, b):
    if r == g == b:
        return (0, 0, r / 255)

    rgb = [None] * 3
    rgb[0] = r / 255
    rgb[1] = g / 255
    rgb[2] = b / 255

    min = rgb[0]
    max = rgb[0]
    maxcolor = 0

    for i in range(len(rgb) - 1):
        if rgb[i + 1] <= min:
            min = rgb[i + 1]
        if rgb[i + 1] >= max:
            max = rgb[i + 1]
            maxcolor = i + 1

    if maxcolor == 0:
        h = (rgb[1] - rgb[2]) / (max - min)
    if maxcolor == 1:
        h = 2 + (rgb[2] - rgb[0]) / (max - min)
    if maxcolor == 2:
        h = 4 + (rgb[0] - rgb[1]) / (max - min)

    if not h:
        h = 0
    h = h * 60
    if h < 0:
        h = h + 360

    l = (min + max) / 2

    if min == max:
        s = 0
    else:
        if l < 0.5:
            s = (max - min) / (max + min)
        else:
            s = (max - min) / (2 - max - min)
    return (h, s, l)
