#!/usr/bin/env python3

import pygame
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *

def main():
    pygame.init()
    
    pygame_clock = pygame.time.Clock()
    pygame_updatable = pygame.sprite.Group()
    pygame_drawable = pygame.sprite.Group()
    pygame_asteroids = pygame.sprite.Group()

    Player.containers = (pygame_updatable, pygame_drawable)
    Asteroid.containers = (pygame_asteroids, pygame_updatable, pygame_drawable)
    AsteroidField.containers = (pygame_updatable)

    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or Player.quit() == True:
                return

        screen.fill(pygame.Color("black"))

        for update in pygame_updatable:
            update.update(dt)

        for draw in pygame_drawable:
            draw.draw(screen)

        pygame.display.flip()

        dt = pygame_clock.tick(60) / 1000


try:
    main()
except IOError as e:
    if e.errno == errno.EPIPE:
        # Support pipeline
        pass
finally:
    pygame.display.quit()
    pygame.quit()