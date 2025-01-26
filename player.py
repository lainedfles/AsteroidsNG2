import base64
import pygame
from audiodata import LASER
from circleshape import CircleShape
from constants import *
from imagedata import SHIP_IMAGE
from io import BytesIO
from shot import Shot

class Player(CircleShape):
    pygame.mixer.init(11025)

    ship = pygame.image.load(BytesIO(base64.b64decode(SHIP_IMAGE)))
    laser = pygame.mixer.Sound(BytesIO(base64.b64decode(LASER)))
    enable_sounds = True

    pygame.mixer.Sound.set_volume(laser, 0.5)

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0
        self.button_timer = 0.1

    def draw(self, screen, enable_graphics):
        if enable_graphics == True:
            player = pygame.draw.polygon(screen, pygame.Color("red"), self.triangle(), -1)
            image = pygame.transform.rotate(Player.ship, -self.rotation)
            screen.blit(image, image.get_rect(centerx = player.centerx, centery = player.centery))
        else:
            pygame.draw.polygon(screen, pygame.Color("red"), self.triangle(), 2)
        
    def move(self, dt):
        self.position += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SPEED * dt

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def shoot(self):
        if self.cooldown_timer > 0:
            return
        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        if Player.enable_sounds:
            pygame.mixer.Sound.play(Player.laser)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.cooldown_timer -= dt
        self.button_timer -= dt
        if self.button_timer <= 0:
            self.button_timer = 0.1

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