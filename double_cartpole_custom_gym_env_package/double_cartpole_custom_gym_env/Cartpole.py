import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import pygame

class Cart():

    def __init__(self, x, y, a, b, mass, RGB, space):
        self.shape = pymunk.Poly.create_box(None, size=(a, b))
        self.moment_of_inertia = pymunk.moment_for_poly(mass, self.shape.get_vertices())
        self.body = pymunk.Body(mass, self.moment_of_inertia, body_type=pymunk.Body.DYNAMIC)
        self.shape.body = self.body
        self.body.position = x, y
        self.shape.color = pygame.Color(RGB)
        self.shape.sensor = True
        space.add(self.body, self.shape)

class Pole():

    def __init__(self, x1, y1, x2, y2, thickness, mass, RGB, space):
        x = (x1+x2)/2
        y = (y1+y2)/2
        length = abs(Vec2d(x1-x2, y1-y2))
        v_vec = Vec2d(x1-x, y1-y)
        x_vec = Vec2d(1, 0)
        angle = Vec2d.get_angle_between(x_vec, v_vec)

        self.shape = pymunk.Poly.create_box(None, size=(length+thickness, thickness))
        self.moment_of_inertia = pymunk.moment_for_poly(mass, self.shape.get_vertices())
        self.body = pymunk.Body(mass, self.moment_of_inertia, body_type=pymunk.Body.DYNAMIC)
        self.shape.body = self.body
        self.body.position = x, y
        self.body.angle = angle
        self.shape.color = pygame.Color(RGB)
        self.shape.sensor = True
        space.add(self.body, self.shape)

class Track():

    def __init__(self, x1, y1, x2, y2, thickness, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (x1, y1), (x2, y2), thickness)
        self.shape.sensor = True
        space.add(self.body, self.shape)
