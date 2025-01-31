#!/usr/bin/env python3

import asyncio
import pygame
import sys
from constants import *
from explosion import Explosion
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shot import Shot

# Global vars
enable_background = enable_graphics = enable_music = enable_sounds = True
enable_help = game_over = music_playing = pause_game = paused = False
game_name = f"AsteroidsNG2"
dt = 0
high_score = 0
old_high_score = 0
score = 0
old_score = 0
time_elapsed = 0
old_time_elapsed = 0
volume = 0.20
death_count = 0

pygame.init()
pygame.mixer.init(11025)
pygame.display.set_icon(pygame.image.load("img/favicon.png"))
pygame.display.set_caption(game_name)

asteroids = pygame.sprite.Group()
drawable = pygame.sprite.Group()
explosions = pygame.sprite.Group()
updatable = pygame.sprite.Group()
shots = pygame.sprite.Group()

clock = pygame.time.Clock()

background_img = pygame.image.load("img/asteroids_background.jpg")

explosion_sfx = pygame.mixer.Sound("sfx/ExploLowFireDest SDT2021805.ogg")
music = pygame.mixer.music.load("sfx/Short Space Casual Loop #3.ogg")
ship_explosion_sfx = pygame.mixer.Sound("sfx/ExploSciFiPipeEx SDT2020802.ogg")
sounds = [explosion_sfx, ship_explosion_sfx]

pygame.mixer.Sound.set_volume(explosion_sfx, volume)
pygame.mixer.music.set_volume(volume)
pygame.mixer.Sound.set_volume(ship_explosion_sfx, volume)

Asteroid.containers = (asteroids, updatable, drawable)
AsteroidField.containers = (updatable)
Explosion.containers = (updatable, drawable)
Player.containers = (updatable, drawable)
Shot.containers = (shots, updatable, drawable)

asteroidfield = AsteroidField()
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


async def main():

    global enable_background, enable_graphics, enable_music, enable_sounds
    global enable_help, game_over, music_playing, pause_game, paused, game_name
    global dt, high_score, old_high_score, score, old_score, time_elapsed
    global old_time_elapsed, volume, death_count, asteroids, drawable, explosions
    global updatable, shots, clock, background_img, explosion_sfx, music
    global ship_explosion_sfx, sounds, asteroidfield, player, screen


    print(f"Starting {game_name}!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print("Press 't' to terminate (exit)...")

    def display_text(input1, input2=[]):
        blits = []
        input, color, font_size = input1
        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, True)
        text = pygame.font.Font.render(font, input, True, color)
        rect = text.get_rect()
        rect.center = (
            (SCREEN_WIDTH / 2),
            (SCREEN_HEIGHT / 2 / 2 / 2)
        )
        blits.append((text, rect))

        spacing = font_size
        for value in input2:
            input, color, font_size = value
            font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, False)
            text = pygame.font.Font.render(font, input, True, color)
            rect = text.get_rect()
            if input2.index(value) > 0:
                spacing += (font_size - 5)
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

        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, bold=True)
        text = pygame.font.Font.render(font, f"Volume {round(volume, 1)}", True, pygame.Color("darkorange"))
        rect = text.get_rect()
        rect.centerx, rect.bottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT)
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
                if keys[pygame.K_MINUS]:
                    volume -= 0.10
                    if volume < 0.00:
                        volume = 0.00
                    pygame.mixer.music.set_volume(volume)
                    for sound in sounds:
                        pygame.mixer.Sound.set_volume(sound, volume)
                if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
                    volume += 0.10
                    if volume > 1.00:
                        volume = 1.00
                    pygame.mixer.music.set_volume(volume)
                    for sound in sounds:
                        pygame.mixer.Sound.set_volume(sound, volume)
                if keys[pygame.K_b]:
                    enable_background = not enable_background
                if keys[pygame.K_g]:
                    enable_graphics = not enable_graphics
                    enable_background = enable_graphics
                if keys[pygame.K_h]:
                    if not game_over and not paused:
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
                    if not game_over and not enable_help:
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
                    old_time_elapsed = time_elapsed
                    time_elapsed = 0
                    game_over = False

                    del asteroids, drawable, updatable
                    del shots, asteroidfield, player

                    asteroids = pygame.sprite.Group()
                    drawable = pygame.sprite.Group()
                    explosions = pygame.sprite.Group()
                    updatable = pygame.sprite.Group()
                    shots = pygame.sprite.Group()

                    Asteroid.containers = (asteroids, updatable, drawable)
                    AsteroidField.containers = (updatable)
                    Explosion.containers = (updatable, drawable)
                    Player.containers = (updatable, drawable)
                    Shot.containers = (shots, updatable, drawable)

                    asteroidfield = AsteroidField()
                    AsteroidField.asteroid_count = 0
                    #Asteroid.asteroids = []
                    dt = 0
                    score = 0
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                if keys[pygame.K_t]:
                    if sys.platform == "emscripten":
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()
                    return

        screen.fill(pygame.Color("black"))

        if enable_music:
            if not music_playing:
                pygame.mixer.music.play(-1)
                music_playing = True

        if enable_background:
            screen.blit(background_img, (0, 0))
            alpha = 200
            if pause_game or game_over:
                alpha = 100
            background_img.set_alpha(alpha)
            screen.convert_alpha()

        if not pause_game:
            for update in updatable:
                update.update(dt, volume)

        for draw in drawable:
            draw.draw(screen, enable_graphics)

        display_hud()
        display_footer()

        if not pause_game:
            for asteroid in asteroids:
                if player.collision(asteroid) and player.alive():
                    if enable_sounds:
                        pygame.mixer.Sound.play(ship_explosion_sfx)
                    Explosion(player.position.x, player.position.y, [pygame.Color("orangered4"),
                                    pygame.Color("orangered3"),
                                    pygame.Color("orangered2"),
                                    pygame.Color("orangered1"),
                                    pygame.Color("orangered")], 120)
                    player.kill()
                    asteroid.split()
                    game_over = True
                    death_count += 1
                    

                for bullet in shots:
                    if asteroid.collision(bullet):
                        score += 1
                        if score > high_score:
                            high_score = score
                        if enable_sounds:
                            pygame.mixer.Sound.play(explosion_sfx)
                        Explosion(asteroid.position.x, asteroid.position.y)
                        AsteroidField.asteroid_count -= 1
                        asteroid.split()
                        bullet.kill()
        elif pause_game and paused:
            display_text((f"PAUSED", pygame.Color("red"), 85), [(f"Time elapsed: {round(time_elapsed)}", pygame.Color("gray50"), round(85 * 0.6)),
                                                                (f"Death count: {death_count}", pygame.Color("crimson"), round(85 * 0.6)),])

        if game_over and not pause_game:
            score_status = [(f"Lasted for {round(time_elapsed)} seconds...", pygame.Color("gray70"), round(85 * 0.6))]

            if score > 0:
                if high_score > old_high_score:
                    score_status.append((f"You've exceeded the high score, well done!", pygame.Color("gold"), round(85 * 0.6)))
                if score > old_score:
                    score_status.append((f"You've surpassed your previous score!", pygame.Color("silver"), round(85 * 0.6)))
                if time_elapsed > old_time_elapsed:
                    score_status.append((f"You've lived longer this round!", pygame.Color("silver"), round(85 * 0.6)))
            else:
                score_status.append((f"You've failed to reach the high score, try again!", pygame.Color("darkred"), round(85 * 0.6)))

            display_text((f"GAME OVER!", pygame.Color("red"), 85), score_status + [(f"", pygame.Color("black"), round(85 * 0.6)),
                                                                                   (f"{death_count} deaths", pygame.Color("crimson"), round(85 * 0.6)),
                                                                                   (f"", pygame.Color("black"), round(85 * 0.6)),
                                                                                   (f"Use the 'n' key to begin a new game", pygame.Color("gray50"), round(85 * 0.6)),
                                                                                   (f"or", pygame.Color("gray40"), round(85 * 0.6)),
                                                                                   (f"use the 't' key to terminate (exit) the game", pygame.Color("gray50"), round(85 * 0.6))])

        if enable_help and not paused:
            display_text((f"KEY CONTROLS", pygame.Color("red"), 85), [(f"[w|a|s|d]: ship movement", pygame.Color("gray70"), round(85 * 0.6)),
                                                                      (f"shift: ship boost", pygame.Color("gray70"), round(85 * 0.6)),
                                                                      (f"space: fire ship blaster", pygame.Color("gray70"), round(85 * 0.6)),
                                                                      (f"", pygame.Color("black"), 20),
                                                                      (f"[-|+]: set volume level", pygame.Color("gray"), round(85 * 0.6)),
                                                                      (f"b: toggle background image", pygame.Color("gray50"), round(85 * 0.6)),
                                                                      (f"g: toggle graphics for a retro look", pygame.Color("gray50"), round(85 * 0.6)),
                                                                      (f"h: display this screen", pygame.Color("gray50"), round(85 * 0.6)),
                                                                      (f"m: toggle music", pygame.Color("gray50"), round(85 * 0.6)),
                                                                      (f"k: toggle sound effects", pygame.Color("gray50"), round(85 * 0.6)),
                                                                      (f"n: new game", pygame.Color("gray"), round(85 * 0.6)),
                                                                      (f"t: terminate (exit) game", pygame.Color("gray"), round(85 * 0.6))])

        pygame.display.flip()

        if pause_game:
            clock.tick(30)
        else:
            dt = clock.tick(60) / 1000
            if not paused and not game_over:
                time_elapsed += dt

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