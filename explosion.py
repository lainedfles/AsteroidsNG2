import pygame
from circleshape import CircleShape

class Explosion(CircleShape):
    def __init__(self, x, y, color_list=[pygame.Color("lightyellow"),
                                         pygame.Color("lightyellow1"),
                                         pygame.Color("lightyellow2"),
                                         pygame.Color("lightyellow3"),
                                         pygame.Color("lightyellow4")], radius=60):
        super().__init__(x, y, radius)
        frames_total = 10
        self.color = color_list[0]
        self.color_list = color_list
        self.color_index = 0
        self.counter = 0
        self.frames = frames_total
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.radius_frame = radius / frames_total

    def update(self, dt, volume):
        self.counter += dt
        self.frames -= dt
        self.radius -= self.radius_frame

        if self.counter >= 2:
            self.color_index += 1
            self.counter = 0
            if self.color_index < len(self.color_list):
                self.color.update(self.color_list[self.color_index])

        if self.frames <= 0:
            self.kill()

    def draw(self, screen, enable_graphics):
        width = 2
        if enable_graphics:
            width = 0
        pygame.draw.circle(screen, self.color, self.position, self.radius, width)