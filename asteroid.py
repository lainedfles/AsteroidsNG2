import base64
import pygame
import math
import random
from player import Player
from circleshape import CircleShape
from constants import *
from imagedata import ASTEROID_IMAGES
from io import BytesIO

class Asteroid(CircleShape):
    asteroids = []
    for i in range(0, len(ASTEROID_IMAGES)):
        asteroids.append(pygame.image.load(BytesIO(base64.b64decode(ASTEROID_IMAGES[i]))))

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.asteroid_variety = random.randint(0, len(Asteroid.asteroids) - 1)
        self.radius = radius
        self.vertex_count = random.randint(5, 12)

    def draw(self, screen, enable_graphics):
        if enable_graphics == True:
            asteroid = pygame.draw.polygon(screen, pygame.Color("darkgrey"), self.polygon(), -1)
            image = pygame.transform.scale(Asteroid.asteroids[self.asteroid_variety], (self.radius * 2, self.radius * 2))
            screen.blit(image, image.get_rect(centerx = asteroid.centerx - self.radius, centery = asteroid.centery))
        else:
            pygame.draw.polygon(screen, pygame.Color("darkgrey"), self.polygon(), 2)

    def polygon(self):
        shape = []
        for i in range(self.vertex_count):
            shape.append(
                [
                    self.position.x + self.radius * math.cos(2 * math.pi * i / self.vertex_count),
                    self.position.y + self.radius * math.sin(2 * math.pi * i / self.vertex_count)
                ]
            )
        return shape

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