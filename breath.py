import canvas
import time
import timeit
import sys
from helpers import normalize_color, ease, calc_coordinates_on_circle, hsl_to_rgb, rgb_to_hsl, rgb_rotate_color_angle, draw_text, get_remaining_frame_time, get_rgb_color_for_number, get_fps


OUTLINE_MODE = True
LOGGING = False
FPS_COUNTER = True

FPS = 60
WIDTH = 1000
HEIGHT = 512
CENTER = {'x': WIDTH / 2, 'y': HEIGHT / 2}

SIMULATION_LENGTH = 10000
CIRCLE_NUMBER = 64
INITIAL_CIRCLE_SIZE = 1
CIRCLE_MAX_SCALE_FACTOR = 200
CIRCLE_PATH_MAX_RADIUS = 200
CIRCLE_PATH_RADIUS_CHANGE_SPEED = 10
CIRCLE_SCALE_SPEED = 8
ROTATION_SPEED = 2

COLOR_OPACITY = 1
AUTO_OPACITY = True
RICH_COLORS_MODE = True
DYNAMIC_COLOR = True

if AUTO_OPACITY:
    COLOR_OPACITY = 1 / (1 + (1 / CIRCLE_NUMBER**2)) if OUTLINE_MODE else 1 / (
        CIRCLE_NUMBER / 4)

COLORS = {
    'white': (255, 255, 255, 1),
    'black': (0, 0, 0, 1),
    'purple': (152, 89, 177, 1),
    'purple-alpha': (152, 89, 177, COLOR_OPACITY),
    'cyan-alpha': (115, 220, 255, COLOR_OPACITY),
    'lightblue-alpha': (0, 0, 255, COLOR_OPACITY)
}


def log(*args, **kwargs):
    if LOGGING:
        end = '\n'
        if kwargs.get('end'):
            end = kwargs['end']

        result = ''
        for arg in args:
            result += str(arg) + ' '
        result += end
        sys.stdout.write(result)


def set_background(color):
    canvas.set_fill_color(*color)
    canvas.fill_rect(0, 0, WIDTH, HEIGHT)


class Circle:

    def __init__(self, canvas: canvas, center_x, center_y, radius, color):
        self.canvas = canvas
        self.radius = radius
        self.__scale_factor = 1
        self.__color = color
        self.center_x = center_x
        self.center_y = center_y

    def _convert_coords(self, x, y, radius):
        '''Convert coordinates from centeralized version (center_x, center_y, radius)
        to canvas style (start_x, start_y, end_x, end_y) - draw inside rectangle'''
        height = width = radius * 2

        return (x - radius, y - radius, height, width)

    def set_coords(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y

    def move(self, move_x, move_y):
        self.center_x += move_x
        self.center_y += move_y

    def rotate_color_angle(self, degrees):
        self.__color = rgb_rotate_color_angle(self.__color, degrees)

    def scale(self, relative=None, absolute=1):
        if relative:
            self.__scale_factor += relative
        else:
            self.__scale_factor = absolute

    def set_color(self, color):
        self.__color = color

    def draw(self):
        if OUTLINE_MODE:
            self.canvas.set_stroke_color(*normalize_color(self.__color))
            self.canvas.draw_ellipse(*self._convert_coords(
                self.center_x, self.center_y, self.radius * self.__scale_factor))
            self.canvas.set_fill_color(*normalize_color(COLORS['white']))
            self.canvas.fill_ellipse(self.center_x, self.center_y, 1, 1)
        else:
            self.canvas.set_fill_color(*normalize_color(self.__color))
            self.canvas.fill_ellipse(*self._convert_coords(
                self.center_x, self.center_y, self.radius * self.__scale_factor))

