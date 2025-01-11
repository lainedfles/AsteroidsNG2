import pygame
from player import Player
from constants import *

def main():
    pygame.init()
    
    pygame_clock = pygame.time.Clock()
    
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(pygame.Color("black"))

        player.update(dt)
        player.draw(screen)

        pygame.display.flip()

        dt = pygame_clock.tick(60) / 1000

try:
    main()
except IOError as e:
    if e.errno == errno.EPIPE:
        # Support pipeline
        pass