#!/usr/bin/env python3

import base64
import pygame
from constants import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from audiodata import MUSIC, EXPLOSION
from imagedata import BACKGROUND_IMAGE
from io import BytesIO
from player import Player
from shot import Shot

def main():
    # Global vars
    enable_background = enable_graphics = enable_music = enable_sounds = True
    enable_help = game_over = music_playing = pause_game = False

    dt = 0
    high_score = 0
    score = 0

    pygame.init()
    pygame.mixer.init(11025)

    asteroids = pygame.sprite.Group()
    background = pygame.image.load(BytesIO(base64.b64decode(BACKGROUND_IMAGE)))
    clock = pygame.time.Clock()
    drawable = pygame.sprite.Group()
    explosion = pygame.mixer.Sound(BytesIO(base64.b64decode(EXPLOSION)))
    music = pygame.mixer.music.load(BytesIO(base64.b64decode(MUSIC)))
    updatable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    asteroidfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.mixer.Sound.set_volume(explosion, 0.5)


    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print("Press 'CTRL + q' to exit...")

    def display_text(input1, input2=[]):
        blits = []
        font_size = 85
        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, bold=True)
        text = pygame.font.Font.render(font, input1, True, pygame.Color("red"))
        rect = text.get_rect()
        rect.center = (
            (SCREEN_WIDTH / 2),
            (SCREEN_HEIGHT / 2 / 2 / 2)
        )
        blits.append((text, rect))

        spacing = font_size
        for input in input2:
            font = pygame.font.SysFont(pygame.font.get_default_font(), round(font_size * 0.6), bold=False)
            text = pygame.font.Font.render(font, input, True, pygame.Color("red"))
            rect = text.get_rect()
            if input2.index(input) > 0:
                spacing += (round(font_size * 0.6) - 5)
            rect.center = (
                (SCREEN_WIDTH / 2),
                ((SCREEN_HEIGHT / 2 / 2 / 2) + spacing)
            )
            blits.append((text, rect))

        screen.blits(blits)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_b]:
                    enable_background = not enable_background
                if keys[pygame.K_g]:
                    enable_graphics = not enable_graphics
                    enable_background = enable_graphics
                if keys[pygame.K_m]:
                    enable_music = not enable_music
                    if not enable_music:
                        pygame.mixer.music.stop()
                        music_playing = False
                if not keys[pygame.K_LCTRL] and keys[pygame.K_n]:
                    enable_sounds = not enable_sounds
                    Player.enable_sounds = enable_sounds
                    if not enable_background:
                        pygame.mixer.stop()
                if keys[pygame.K_p]:
                    pause_game = not pause_game
                    if pause_game:
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                if keys[pygame.K_LCTRL] and keys[pygame.K_n]:
                    game_over = False

                    del asteroids, drawable, updatable
                    del shots, asteroidfield, player

                    asteroids = pygame.sprite.Group()
                    drawable = pygame.sprite.Group()
                    updatable = pygame.sprite.Group()
                    shots = pygame.sprite.Group()

                    Asteroid.containers = (asteroids, updatable, drawable)
                    AsteroidField.containers = (updatable)
                    Player.containers = (updatable, drawable)
                    Shot.containers = (shots, updatable, drawable)

                    asteroidfield = AsteroidField()
                    dt = 0
                    score = 0
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                if keys[pygame.K_LCTRL] and keys[pygame.K_q]:
                    return

        screen.fill(pygame.Color("black"))

        if enable_music:
            if not music_playing:
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.25)
                music_playing = True

        if enable_background:
            screen.blit(background, (0, 0))
            alpha = 200
            if pause_game or game_over:
                alpha = 100
            background.set_alpha(alpha)
            screen.convert_alpha()

        if not pause_game:
            for update in updatable:
                update.update(dt)

        for draw in drawable:
            draw.draw(screen, enable_graphics)

        if not pause_game:
            for asteroid in asteroids:
                if player.collision(asteroid):
                    player.kill()
                    game_over = True

                for bullet in shots:
                    if asteroid.collision(bullet):
                        score += 1
                        if score > high_score:
                            high_score = score
                        if enable_sounds:
                            pygame.mixer.Sound.play(explosion)
                        asteroid.split()
                        bullet.kill()
        else:                    
            display_text(f"PAUSED", [f"Current score: {score}", f"High score: {high_score}"])

        if game_over and not pause_game:
            display_text(f"GAME OVER!", [f"Current score: {score}",
                                         f"High score: {high_score}",
                                         f"",
                                         f"Use 'CTRL + n' to begin a new game",
                                         f"or",
                                         f"'CTRL + q' to quit"])

        pygame.display.flip()

        if pause_game:
            clock.tick(10)
        else:
            dt = clock.tick(60) / 1000


try:
    main()
except IOError as e:
    if e.errno == errno.EPIPE:
        # Support pipeline
        pass
finally:
    pygame.display.quit()
    pygame.quit()