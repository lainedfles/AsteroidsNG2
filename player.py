import pygame
import math
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    pygame.mixer.init(11025)

    ship = pygame.image.load("img/asteroids_ship_small.png")
    laser = pygame.mixer.Sound("sfx/Sci-Fi-Laser_GEN-HD4-43659.ogg")
    booster = pygame.mixer.Sound("sfx/Whoosh-Spaceship_Whoosh-Flying-Spaceship-Rocket_SDT3-2075.ogg")
    enable_sounds = True

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.boost_duration = PLAYER_SPEED_BOOST_DURATION
        self.boost_color = pygame.Color("orange")
        self.boost_cooldown_timer = 0
        self.button_timer = 0.1
        self.cooldown_timer = 0
        self.enable_boost = False
        self.player_speed = PLAYER_SPEED
        self.rotation = 0
        self.volume = 0.25

    def boost(self):
        if self.boost_cooldown_timer > 0:
            return

        self.boost_cooldown_timer = PLAYER_SPEED_BOOST_COOLDOWN
        self.enable_boost = True
        self.player_speed += PLAYER_SPEED_BOOST

        if Player.enable_sounds:
            pygame.mixer.Sound.set_volume(Player.booster, self.volume)
            pygame.mixer.Sound.play(Player.booster)

    def draw(self, screen, enable_graphics):
        if enable_graphics == True:
            player = pygame.draw.polygon(screen, pygame.Color("red"), self.triangle(self.position, self.radius, self.rotation), -1)
            image = pygame.transform.rotate(Player.ship, -self.rotation)
            screen.blit(image, image.get_rect(centerx = player.centerx, centery = player.centery))

            if self.enable_boost:
                pygame.draw.polygon(screen, self.boost_color, self.triangle_rotate(player.center, self.triangle((player.centerx + 15, player.centery - 65), self.radius / 3, 0), math.radians(self.rotation)), 0)
                pygame.draw.polygon(screen, self.boost_color, self.triangle_rotate(player.center, self.triangle((player.centerx, player.centery - 60), self.radius / 3, 0), math.radians(self.rotation)), 0)
                pygame.draw.polygon(screen, self.boost_color, self.triangle_rotate(player.center, self.triangle((player.centerx - 15, player.centery - 65), self.radius / 3, 0), math.radians(self.rotation)), 0)
        else:
            player = pygame.draw.polygon(screen, pygame.Color("red"), self.triangle(self.position, self.radius, self.rotation), 2)
            pygame.draw.polygon(screen, pygame.Color("orangered"), self.triangle(self.position, self.radius / 3, self.rotation), 2)

            if self.enable_boost:
                pygame.draw.polygon(screen, self.boost_color, self.triangle_rotate(player.center, self.triangle((player.centerx + 15, player.centery - 35), self.radius / 3, 0), math.radians(self.rotation)), 2)
                pygame.draw.polygon(screen, self.boost_color, self.triangle_rotate(player.center, self.triangle((player.centerx, player.centery - 30), self.radius / 3, 0), math.radians(self.rotation)), 2)
                pygame.draw.polygon(screen, self.boost_color, self.triangle_rotate(player.center, self.triangle((player.centerx - 15, player.centery - 35), self.radius / 3, 0), math.radians(self.rotation)), 2)

        
    def move(self, dt):
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT
        self.position += pygame.Vector2(0, 1).rotate(self.rotation) * self.player_speed * dt

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def shoot(self):
        if self.cooldown_timer > 0:
            return
        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        if Player.enable_sounds:
            pygame.mixer.Sound.set_volume(Player.laser, self.volume)
            pygame.mixer.Sound.play(Player.laser)

    def triangle(self, position, radius, rotation):
        forward = pygame.Vector2(0, 1).rotate(rotation)
        right = pygame.Vector2(0, 1).rotate(rotation + 90) * radius / 1.5
        a = position + forward * radius
        b = position - forward * radius - right
        c = position - forward * radius + right
        return [a, b, c]

    def triangle_rotate(self, anchor, verticies, angle):
        rotated_verticies = []
        for (x, y) in verticies:
            dx = x - anchor[0]
            dy = y - anchor[1]
            cos_theta = math.cos(angle)
            sin_theta = math.sin(angle)
            new_x = dx * cos_theta - dy * sin_theta
            new_y = dx * sin_theta + dy * cos_theta
            rotated_verticies.append((new_x + anchor[0], new_y + anchor[1]))
        return rotated_verticies

    def update(self, dt, volume):
        self.button_timer -= dt
        self.boost_cooldown_timer -= dt
        self.boost_duration -= dt
        self.cooldown_timer -= dt
        self.volume = volume

        if self.enable_boost:
            if self.boost_color == pygame.Color("orange"):
                self.boost_color = pygame.Color("orange4")
            else:
                self.boost_color = pygame.Color("orange")

        if self.button_timer <= 0:
            self.button_timer = 0.1

        if self.boost_duration <= 0:
            self.enable_boost = False
            self.player_speed = PLAYER_SPEED
            self.boost_duration = PLAYER_SPEED_BOOST_DURATION

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_LSHIFT]:
            self.boost()