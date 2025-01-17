import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color("white"), self.position, self.radius, width=2)

    def split(self):
        random_angle = random.uniform(20, 50)

        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        split1a = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        split1a.velocity = pygame.Vector2(self.velocity).rotate(random_angle) * 1.2

        split2a = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        split2a.velocity = pygame.Vector2(self.velocity).rotate(-random_angle) * 1.2

    def update(self, dt):
        self.position += self.velocity * dt