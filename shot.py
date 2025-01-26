import pygame
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen, enable_graphics):
        width = 2
        if enable_graphics:
            width = 0
        pygame.draw.circle(screen, pygame.Color("yellow"), self.position, self.radius, width)

    def update(self, dt):
        self.position += self.velocity * dt