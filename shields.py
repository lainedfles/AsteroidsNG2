import pygame
from circleshape import CircleShape


class Shields(CircleShape):
    color_index = 0

    def __init__(self, x, y, color_list=[pygame.Color("lightyellow"),
                                         pygame.Color("lightyellow1"),
                                         pygame.Color("lightyellow2"),
                                         pygame.Color("lightyellow3"),
                                         pygame.Color("lightyellow4"),
                                         pygame.Color("lightsalmon"),
                                         pygame.Color("lightsalmon1"),
                                         pygame.Color("lightsalmon2"),
                                         pygame.Color("lightsalmon3"),
                                         pygame.Color("lightsalmon4"),
                                         pygame.Color("lightskyblue"),
                                         pygame.Color("lightskyblue1"),
                                         pygame.Color("lightskyblue2"),
                                         pygame.Color("lightskyblue3"),
                                         pygame.Color("lightskyblue4")], radius=60):
        super().__init__(x, y, radius)
        self.color = color_list[0]
        self.color_list = color_list
        self.frames = 0.1
        self.position = pygame.Vector2(x, y)
        self.max_radius = radius
        self.radius = radius

    def update(self, dt, volume):
        self.frames -= dt

        if self.radius != self.max_radius:
            self.radius = self.max_radius
        else:
            self.radius -= 2

        Shields.color_index += 1
        if Shields.color_index < len(self.color_list) - 1:
            self.color.update(self.color_list[Shields.color_index])
        else:
            Shields.color_index = 0

        if self.frames <= 0:
            self.frames = 0.1
            self.kill()

    def draw(self, screen, enable_graphics):
        width = 1
        pygame.draw.circle(screen, self.color, self.position, self.radius, width)