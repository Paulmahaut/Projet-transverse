import pygame as py

class Platform(py.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Initialize platform attributes
        self.image = py.Surface((width, height))
        self.image.fill((255, 255, 255))  # White color for now
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y