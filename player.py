import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    player_quit = False
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0
        
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, pygame.Color("white"), self.triangle(), width=2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
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
            if self.cooldown_timer > 0:
                self.cooldown_timer -= dt
            elif self.cooldown_timer <= 0:
                self.shoot()
        if keys[pygame.K_LCTRL] and keys[pygame.K_q]:
            Player.player_quit = True

    def move(self, dt):
        self.position += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SPEED * dt

    def shoot(self):
        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN
        player_pos = self.position
        shot = Shot(player_pos[0], player_pos[1], SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def quit():
        return Player.player_quit