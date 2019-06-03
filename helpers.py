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

