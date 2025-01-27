#!/usr/bin/env python3

import asyncio
import pygame
from constants import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shot import Shot

# Global vars
enable_background = enable_graphics = enable_music = enable_sounds = True
enable_help = game_over = music_playing = pause_game = paused = False
game_name = f"AsteroidsNG2"

async def main():
    dt = 0
    high_score = 0
    old_high_score = 0
    score = 0
    old_score = 0

    global enable_background, enable_graphics, enable_music, enable_sounds
    global enable_help, game_over, music_playing, pause_game, paused, game_name

    pygame.init()
    pygame.mixer.init(11025)
    pygame.display.set_icon(pygame.image.load("img/favicon.png"))
    pygame.display.set_caption(game_name)

    asteroids = pygame.sprite.Group()
    background_image = pygame.image.load("img/asteroids_background.jpg")
    clock = pygame.time.Clock()
    drawable = pygame.sprite.Group()
    explosion = pygame.mixer.Sound("sfx/ExploLowFireDest SDT2021805.ogg")
    music = pygame.mixer.music.load("sfx/Short Space Casual Loop #3.ogg")
    updatable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    ship_explosion = pygame.mixer.Sound("sfx/ExploSciFiPipeEx SDT2020802.ogg")

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    asteroidfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.mixer.Sound.set_volume(explosion, 0.35)
    pygame.mixer.Sound.set_volume(ship_explosion, 0.35)


    print(f"Starting {game_name}!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print("Press 't' to terminate (exit)...")

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

    def display_hud():
        blits = []
        font_size = 40
        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, bold=False)
        text = pygame.font.Font.render(font, f"High Score: {high_score}", True, pygame.Color("darkorange"))
        rect = text.get_rect()
        rect.x, rect.y = (0, 0)
        blits.append((text, rect))

        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, bold=True)
        text = pygame.font.Font.render(font, f"{game_name}", True, pygame.Color("darkgrey"))
        rect = text.get_rect()
        rect.centerx, rect.y = ((SCREEN_WIDTH / 2), 0)
        blits.append((text, rect))

        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, bold=False)
        text = pygame.font.Font.render(font, f"Current Score: {score}", True, pygame.Color("darkgreen"))
        rect = text.get_rect()
        rect.right, rect.y = (SCREEN_WIDTH, 0)
        blits.append((text, rect))

        screen.blits(blits)

    def display_footer():
        blits = []
        font_size = 30
        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, bold=False)
        text = pygame.font.Font.render(font, f"Press 'h' for help", True, pygame.Color("darkred"))
        rect = text.get_rect()
        rect.x, rect.bottom = (0, SCREEN_HEIGHT)
        blits.append((text, rect))

        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, bold=False)
        text = pygame.font.Font.render(font, f"Press 'g' for a retro look", True, pygame.Color("darkred"))
        rect = text.get_rect()
        rect.right, rect.bottom = (SCREEN_WIDTH, SCREEN_HEIGHT)
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
                if keys[pygame.K_h]:
                    pause_game = not pause_game
                    enable_help = pause_game
                    if pause_game:
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                if keys[pygame.K_m]:
                    enable_music = not enable_music
                    if not enable_music:
                        pygame.mixer.music.stop()
                        music_playing = False
                if keys[pygame.K_k]:
                    enable_sounds = not enable_sounds
                    Player.enable_sounds = enable_sounds
                    if not enable_background:
                        pygame.mixer.stop()
                if keys[pygame.K_p]:
                    pause_game = not pause_game
                    paused = pause_game
                    if pause_game:
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                if keys[pygame.K_n]:
                    old_score = score
                    old_high_score = high_score
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
                if keys[pygame.K_t]:
                    return

        screen.fill(pygame.Color("black"))

        if enable_music:
            if not music_playing:
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.25)
                music_playing = True

        if enable_background:
            screen.blit(background_image, (0, 0))
            alpha = 200
            if pause_game or game_over:
                alpha = 100
            background_image.set_alpha(alpha)
            screen.convert_alpha()

        if not pause_game:
            for update in updatable:
                update.update(dt)

        for draw in drawable:
            draw.draw(screen, enable_graphics)

        display_hud()
        display_footer()

        if not pause_game:
            for asteroid in asteroids:
                if player.collision(asteroid) and player.alive():
                    if enable_sounds:
                        pygame.mixer.Sound.play(ship_explosion)
                    player.kill()
                    asteroid.split()
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
        elif pause_game and paused:
            display_text(f"PAUSED", [f"Current score: {score}", f"High score: {high_score}"])

        if game_over and not pause_game:
            score_status = [f"You've failed to reach the high score, try again!"]

            if score > 0:
                if high_score > old_high_score:
                    score_status = []
                    score_status.append(f"You've exceeded the high score, well done!")
                if score > old_score:
                    score_status.append(f"You've surpassed your previous score!")

            display_text(f"GAME OVER!", score_status + [f"",
                                                        f"Use the 'n' key to begin a new game",
                                                        f"or",
                                                        f"use the 't' key to terminate (exit) the game"])

        if enable_help and not paused:
            display_text(f"KEY CONTROLS", [f"b: toggle background image",
                                           f"g: toggle graphics for a retro look",
                                           f"h: display this screen",
                                           f"m: toggle music",
                                           f"k: toggle sound effects",
                                           f"n: new game",
                                           f"t: terminate (exit) game"])

        pygame.display.flip()

        if pause_game:
            clock.tick(10)
        else:
            dt = clock.tick(60) / 1000

        await asyncio.sleep(0)


try:
    asyncio.run(main())
except IOError as e:
    if e.errno == errno.EPIPE:
        # Support pipeline
        pass
finally:
    pygame.display.quit()
    pygame.quit()