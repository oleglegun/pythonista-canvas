import canvas
import time
import random
import helpers
import math
import time


PARTICLE_COUNT = 1000
GENERATOR_HEIGHT_PERCENT = 90
PARTICLE_SIZE = 7
PARTICLE_FORM_ELLIPSE = True
BOUNCE = True
BOUNCE_4_SIDES = False
BOUNCE_VALUE = 40
FPS = 60
GRAVITY = 5
SIMULATION_TIME = 4000
INTIAL_VELOCITY_RANGE = 10
CANVAS_WIDTH = 720
CANVAS_HEIGHT = 480
FADE_IN_EFFECT = False
FADE_OUT_EFFECT = False
FADE_HOLE_DISTANCE = 100
ROTATE_COLOR = True
RANDOM_COLORS = True
WATER_COLORS = False


class Particle:
    def __init__(self, canvas, x, y):
        self._fade_rate = random.randint(1, 10)
        self._x_init = x
        self._y_init = y
        self.canvas = canvas
        self.x = self.x_old = x
        self.y = self.y_old = y

    def set_color(self, color):
        self._color = color
    
    def color(self):
        return self._color

    def distance_from_init_point(self):
        dx = self._x_init - self.x
        dy = self._y_init - self.y
        return math.sqrt(abs(dx ** 2 + dy ** 2))

    def set_intial_velocity(self, dx, dy):
        self.x_old += dx
        self.y_old += dy
    
    def integrate(self):
        velocity_x = self.x - self.x_old
        velocity_y = self.y - self.y_old
        self.x_old = self.x
        self.y_old = self.y
        self.x += velocity_x
        self.y += velocity_y
    
    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y
    
    def fade(self):
        distance = self.distance_from_init_point()
        if distance == 0:
            return
        
        r, g, b, a = self.color()

        opacity = 1

        if FADE_IN_EFFECT and distance < FADE_HOLE_DISTANCE:
            opacity = 1 * distance/(FADE_HOLE_DISTANCE * 10)
        if FADE_OUT_EFFECT:
            opacity = a / (self._fade_rate * (distance/1000))
            
        self.set_color((r, g, b, opacity))

    def draw(self):
        if PARTICLE_FORM_ELLIPSE:
            self.canvas.set_fill_color(*self._color)
            self.canvas.fill_ellipse(self.x_old, self.y_old, PARTICLE_SIZE, PARTICLE_SIZE)
        else:
            self.canvas.set_stroke_color(*self._color)
            self.canvas.set_line_width(PARTICLE_SIZE)
            self.canvas.draw_line(self.x_old, self.y_old, self.x, self.y)
        
    def bounce(self, canvas):
        w, h = canvas.get_size()
        rand = random.randint(-2, 2)
        if self.y < 0: self.y += BOUNCE_VALUE + rand; self.x += rand
        if BOUNCE_4_SIDES:
            if self.y > h: self.y -= BOUNCE_VALUE
            if self.x < 0: self.x += BOUNCE_VALUE /5
            if self.x > w: self.x -= BOUNCE_VALUE /5
        
    def is_outside_canvas(self):
        if self.x > CANVAS_WIDTH or self.x < 0 or self.y > CANVAS_HEIGHT or self.y < 0:
            return True
        return False
