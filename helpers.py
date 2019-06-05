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

def get_rgb_color_for_number(number, total_colors_count=None, opacity=1):
    if total_colors_count is None:
        angle = number % 360
    else:
        angle = 360 * (number / total_colors_count)
    r, g, b = hsl_to_rgb(hue=angle, sat=1, light=0.5)
    return (r, g, b, opacity)

def get_normalized_rgb_color_for_number(*args, **kwargs):
    return normalize_color(get_rgb_color_for_number(*args, **kwargs))

def get_random_rgb_color(degree_start=0, degree_end=360, opacity=1):
    rand = random.randint(degree_start, degree_end)
    rgba = (*hsl_to_rgb(rand, 1, 0.5), opacity)
    return normalize_color(rgba)

def randomize_color_brightness(color):
    r, g, b, a = color
    level = random.random()
    return (r * level, g * level, b * level, a)

def rgb_rotate_color_angle(rgb_color, degrees):
    r, g, b, a = rgb_color
    h, s, l = rgb_to_hsl(r, g, b)
    h = (h + degrees) % 360
    return (*hsl_to_rgb(h, s, l), a)

def draw_text(canvas, text, position='top', color=(255, 255, 255)):
    canvas.set_fill_color(*color)
    w, h = canvas.get_size()
    
    if position == 'top':
        x, y = (5, h - 30)
    elif position == 'bottom':
        x, y = 5, 5

    canvas.draw_text(text, x, y, font_name='Helvetica', font_size=16)

def get_fps(time_start, time_finish):
    time_elapsed = time_finish - time_start
    return round(1 / time_elapsed)

__all__ = [
    normalize_number, normalize_color, ease, calc_coordinates_on_circle,
    hsl_to_rgb, rgb_to_hsl, rgb_rotate_color_angle, draw_text,
    get_remaining_frame_time, get_rgb_color_for_number, get_fps
]

