#!/usr/bin/env python3

import asyncio
import pygame
import sys
from constants import *
from explosion import Explosion
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shields import Shields
from shot import Shot

# Global vars
enable_background = enable_graphics = enable_music = enable_sounds = True
enable_debug = enable_help = game_over = music_playing = pause_game = paused = shields_up = False
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
level = 1
shields_cooldown = PLAYER_SHIELDS_COOLDOWN

pygame.init()
pygame.mixer.init(11025)
pygame.display.set_icon(pygame.image.load("img/favicon.png"))
pygame.display.set_caption(game_name)

asteroids = pygame.sprite.Group()
drawable = pygame.sprite.Group()
explosions = pygame.sprite.Group()
updatable = pygame.sprite.Group()
shields = pygame.sprite.Group()
shots = pygame.sprite.Group()

clock = pygame.time.Clock()

background_img = pygame.image.load("img/asteroids_background.jpg")

explosion_sfx = pygame.mixer.Sound("sfx/ExploLowFireDest SDT2021805.ogg")
shields_up_sfx = pygame.mixer.Sound("sfx/AccentElements PET04_58_8_rev.ogg")
shields_down_sfx = pygame.mixer.Sound("sfx/AccentElements PET04_58_8.ogg")
ship_explosion_sfx = pygame.mixer.Sound("sfx/ExploSciFiPipeEx SDT2020802.ogg")
sounds = [shields_up_sfx, shields_down_sfx, explosion_sfx, ship_explosion_sfx]

music_list = ["sfx/Short Space Casual Loop #3.ogg",
              "sfx/Orchestral Loop #4.ogg",
              "sfx/Loop #3.ogg",
              "sfx/Space Casual Theme #2 (looped).ogg"]
selected_music = music_list[0]

for sound in sounds:
    pygame.mixer.Sound.set_volume(sound, volume)

Asteroid.containers = (asteroids, updatable, drawable)
AsteroidField.containers = updatable
Explosion.containers = (updatable, drawable)
Player.containers = (updatable, drawable)
Shot.containers = (shots, updatable, drawable)
Shields.containers = (updatable, drawable)


async def main():

    global enable_background, enable_graphics, enable_music, enable_sounds
    global enable_help, game_over, music_playing, pause_game, paused, game_name
    global enable_debug, dt, high_score, old_high_score, score, old_score, time_elapsed
    global old_time_elapsed, volume, death_count, asteroids, drawable, explosions
    global updatable, shots, clock, background_img, explosion_sfx, music, ship_explosion_sfx
    global sounds, asteroidfield, player, screen, level, shields_up, shields_cooldown
    global music_list, selected_music

    asteroidfield = AsteroidField()
    music = pygame.mixer.music.load(selected_music)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.mixer.music.set_volume(volume)

    print(f"Starting {game_name}!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print("Press 't' to terminate (exit)...")

    def change_music(direction):
        global music_list, selected_music, volume
        if direction == "left":
            music_index = music_list.index(selected_music) - 1
            if music_index < 0:
                music_index = len(music_list) - 1
            selected_music = music_list[music_index]
        if direction == "right":
            music_index = music_list.index(selected_music) + 1
            if music_index > len(music_list) - 1:
                music_index = 0
            selected_music = music_list[music_index]
        pygame.mixer.music.load(selected_music)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()

    def display_text(input1, input2=[]):
        blits = []
        input, color, font_size = input1
        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, True)
        text = pygame.font.Font.render(font, input, True, color)
        rect = text.get_rect()
        rect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2 / 2 / 2))
        blits.append((text, rect))

        spacing = font_size
        for value in input2:
            input, color, font_size = value
            font = pygame.font.SysFont(pygame.font.get_default_font(), font_size, False)
            text = pygame.font.Font.render(font, input, True, color)
            rect = text.get_rect()
            if input2.index(value) > 0:
                spacing += font_size - 5
            rect.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2 / 2 / 2) + spacing))
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

        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size - 10, bold=False)
        text = pygame.font.Font.render(font, f"{AsteroidField.asteroid_count}", True, pygame.Color("gray52"))
        rect = text.get_rect()
        rect.centerx, rect.y = ((SCREEN_WIDTH / 2), font_size)
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

        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size - 2, bold=True)
        text = pygame.font.Font.render(font, f"Level {round(level)}", True, pygame.Color("lightgoldenrod3"))
        rect = text.get_rect()
        rect.centerx, rect.bottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - font_size)
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
                if keys[pygame.K_LEFTBRACKET]:
                    change_music("left")
                if keys[pygame.K_RIGHTBRACKET]:
                    change_music("right")
                if keys[pygame.K_F1]:
                    enable_debug = not enable_debug
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

                    debug = enable_debug
                    player_ship = Player.ship
                    player_ship_color = Player.ship_color
                    select_music = selected_music

                    del asteroids, drawable, updatable
                    del shots, asteroidfield, player
                    if shields_up:
                        del shields
                        shields_up = False

                    asteroids = pygame.sprite.Group()
                    drawable = pygame.sprite.Group()
                    explosions = pygame.sprite.Group()
                    updatable = pygame.sprite.Group()
                    shields = pygame.sprite.Group()
                    shots = pygame.sprite.Group()

                    Asteroid.containers = (asteroids, updatable, drawable)
                    AsteroidField.containers = updatable
                    Explosion.containers = (updatable, drawable)
                    Player.containers = (updatable, drawable)
                    Shields.containers = (updatable, drawable)
                    Shot.containers = (shots, updatable, drawable)

                    asteroidfield = AsteroidField()
                    AsteroidField.asteroid_count = 0
                    AsteroidField.asteroid_max_spawn = ASTEROID_SPAWN
                    AsteroidField.asteroid_spawn_rate = ASTEROID_SPAWN_RATE

                    dt = 0
                    level = 1
                    score = 0

                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    Player.shoot_speed = PLAYER_SHOOT_SPEED
                    Player.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
                    Player.boost_cooldown = PLAYER_SPEED_BOOST_COOLDOWN
                    Player.ship = player_ship
                    Player.ship_color = player_ship_color
                    selected_music = select_music
                    enable_debug = debug
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
                if shields_up and shields.collision(asteroid):
                    if enable_sounds:
                        pygame.mixer.Sound.play(shields_down_sfx)
                    shields_up = False
                    Explosion(
                        shields.position.x,
                        shields.position.y,
                        [
                            pygame.Color("dodgerblue4"),
                            pygame.Color("dodgerblue3"),
                            pygame.Color("dodgerblue2"),
                            pygame.Color("dodgerblue1"),
                            pygame.Color("dodgerblue"),
                        ],
                        90,
                    )
                    shields.kill()
                    if asteroid.split():
                        AsteroidField.asteroid_count += 2
                elif player.collision(asteroid) and player.alive():
                    if enable_sounds:
                        pygame.mixer.Sound.play(ship_explosion_sfx)
                    Explosion(
                        player.position.x,
                        player.position.y,
                        [
                            pygame.Color("orangered4"),
                            pygame.Color("orangered3"),
                            pygame.Color("orangered2"),
                            pygame.Color("orangered1"),
                            pygame.Color("orangered"),
                        ],
                        120,
                    )
                    player.kill()
                    if asteroid.split():
                        AsteroidField.asteroid_count += 2
                    game_over = True
                    death_count += 1

                for bullet in shots:
                    if asteroid.collision(bullet):
                        score += 1
                        if score > high_score:
                            high_score = score

                        if score >= 20:
                            level = score // 20
                            if AsteroidField.asteroid_max_spawn < ASTEROID_MAX_SPAWN:
                                AsteroidField.asteroid_max_spawn += level / (20 / 3)
                            if AsteroidField.asteroid_spawn_rate > ASTEROID_MIN_SPAWN_RATE:
                                AsteroidField.asteroid_spawn_rate -= level * 0.001
                            if Player.shoot_speed < PLAYER_SHOOT_MAX_SPEED:
                                Player.shoot_speed += level * 1.5
                            if Player.shoot_cooldown > PLAYER_SHOOT_MIN_COOLDOWN:
                                Player.shoot_cooldown -= level * 0.0004
                            if Player.boost_cooldown > PLAYER_SPEED_MIN_BOOST_COOLDOWN:
                                Player.boost_cooldown -= level * 0.0008
                            if shields_cooldown <= 0:
                                shields_cooldown = PLAYER_SHIELDS_COOLDOWN
                                shields_up = True
                                if enable_sounds:
                                    pygame.mixer.Sound.play(shields_up_sfx)
                            if enable_debug:
                                print(
                                    f"level {level} asteroid_max_spawn {AsteroidField.asteroid_max_spawn} asteroid_spawn_rate {AsteroidField.asteroid_spawn_rate}"
                                )
                                print(
                                    f"shoot_speed {Player.shoot_speed} shoot_cooldown {Player.shoot_cooldown} boost_cooldown {Player.boost_cooldown}"
                                )

                        if enable_sounds:
                            pygame.mixer.Sound.play(explosion_sfx)

                        Explosion(asteroid.position.x, asteroid.position.y)
                        AsteroidField.asteroid_count -= 1

                        if asteroid.split():
                            AsteroidField.asteroid_count += 2
                        bullet.kill()
                if shields_up:
                    shields = Shields(
                        player.position.x,
                        player.position.y
                    )
        elif pause_game and paused:
            display_text(
                (f"PAUSED", pygame.Color("red"), 85),
                [
                    (f"Time elapsed: {round(time_elapsed)}", pygame.Color("gray50"), round(85 * 0.6)),
                    (f"Death count: {death_count}", pygame.Color("crimson"), round(85 * 0.6)),
                ],
            )

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
                score_status.append(
                    (f"You've failed to reach the high score, try again!", pygame.Color("darkred"), round(85 * 0.6))
                )

            display_text(
                (f"GAME OVER!", pygame.Color("red"), 85),
                score_status
                + [
                    (f"", pygame.Color("black"), round(85 * 0.6)),
                    (f"{death_count} deaths", pygame.Color("crimson"), round(85 * 0.6)),
                    (f"", pygame.Color("black"), round(85 * 0.6)),
                    (f"Use the 'n' key to begin a new game", pygame.Color("gray50"), round(85 * 0.6)),
                    (f"or", pygame.Color("gray40"), round(85 * 0.6)),
                    (f"use the 't' key to terminate (exit) the game", pygame.Color("gray50"), round(85 * 0.6)),
                ],
            )

        if enable_help and not paused:
            display_text(
                (f"KEY CONTROLS", pygame.Color("red"), 85),
                [
                    (f"w|a|s|d ship movement", pygame.Color("gray70"), round(85 * 0.5)),
                    (f"shift ship boost", pygame.Color("gray70"), round(85 * 0.5)),
                    (f"space fire ship blaster", pygame.Color("gray70"), round(85 * 0.5)),
                    (f"", pygame.Color("black"), 20),
                    (f"-|+ set volume level", pygame.Color("gray"), round(85 * 0.5)),
                    (f",|. change ship appearance", pygame.Color("gray65"), round(85 * 0.5)),
                    (f"[|] select music track", pygame.Color("gray"), round(85 * 0.5)),
                    (f"b toggle background image", pygame.Color("gray50"), round(85 * 0.5)),
                    (f"g toggle graphics for a retro look", pygame.Color("gray50"), round(85 * 0.5)),
                    (f"h display this screen", pygame.Color("gray50"), round(85 * 0.5)),
                    (f"m toggle music", pygame.Color("gray50"), round(85 * 0.5)),
                    (f"k toggle sound effects", pygame.Color("gray50"), round(85 * 0.5)),
                    (f"n new game", pygame.Color("gray"), round(85 * 0.5)),
                    (f"t terminate (exit) game", pygame.Color("gray"), round(85 * 0.5)),
                ],
            )

        pygame.display.flip()

        if pause_game:
            clock.tick(30)
        else:
            dt = clock.tick(60) / 1000
            if not paused and not game_over:
                time_elapsed += dt
                if not shields_up:
                    shields_cooldown -= dt

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