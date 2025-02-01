import pygame
import math
import random
from player import Player
from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    asteroids = []
    asteroid_images = [
        "img/asteroid1_60.png",
        "img/asteroid2_60.png",
        "img/asteroid3_60.png",
        "img/asteroid4_60.png",
        "img/asteroid5_60.png",
        "img/asteroid6_60.png",
        "img/asteroid7_60.png",
        "img/asteroid8_60.png",
    ]
    for i in range(0, len(asteroid_images)):
        asteroids.append(pygame.image.load(asteroid_images[i]))

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.asteroid_variety = random.randint(0, len(Asteroid.asteroids) - 1)
        self.asteroid_color = pygame.Color(f"gray{random.randint(25, 75)}")
        self.radius = radius
        self.vertex_count = random.randint(5, 12)

    def draw(self, screen, enable_graphics):
        if enable_graphics == True:
            asteroid = pygame.draw.polygon(screen, self.asteroid_color, self.polygon(), -1)
            image = pygame.transform.scale(Asteroid.asteroids[self.asteroid_variety], (self.radius * 2, self.radius * 2))
            screen.blit(image, image.get_rect(centerx=asteroid.centerx - self.radius, centery=asteroid.centery))
        else:
            pygame.draw.polygon(screen, self.asteroid_color, self.polygon(), 2)

    def polygon(self):
        shape = []
        for i in range(self.vertex_count):
            shape.append(
                [
                    self.position.x + self.radius * math.cos(2 * math.pi * i / self.vertex_count),
                    self.position.y + self.radius * math.sin(2 * math.pi * i / self.vertex_count),
                ]
            )
        return shape

    def split(self):
        random_angle = random.uniform(20, 50)

        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return False

        split1a = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        split1a.velocity = pygame.Vector2(self.velocity).rotate(random_angle) * 1.2

        split2a = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        split2a.velocity = pygame.Vector2(self.velocity).rotate(-random_angle) * 1.2

        return True

    def update(self, dt, volume):
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT
        self.position += self.velocity * dt