import pygame as py

class Platform(py.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Initialize platform attributes
        image = py.image.load("images/cloud1.png").convert_alpha()
        self.image = py.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
