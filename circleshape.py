import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def collision(self, object: "CircleShape"):
        combined_radius = self.radius + object.radius
        distance = self.position.distance_to(object.position)
        if distance <= combined_radius:
            return True
        return False

    def draw(self, screen, enable_graphics):
        # sub-classes must override
        pass

    def update(self, dt, volume):
        # sub-classes must override
        pass