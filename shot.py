import pygame
from circleshape import CircleShape
from constants import *


class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.radius = radius
        self.expiration = 0.8

    def draw(self, screen, enable_graphics):
        width = 2
        if enable_graphics:
            width = 0
        pygame.draw.circle(screen, pygame.Color("yellow"), self.position, self.radius, width)

    def update(self, dt, volume):
        self.expiration -= dt
        if self.expiration <= 0:
            self.kill()
        else:
            self.position.x %= SCREEN_WIDTH
            self.position.y %= SCREEN_HEIGHT
            self.position += self.velocity * dt