import pygame as py
import random

class Mushspawn():
    def __init__(self):
        # Load the image
        original_image = py.image.load("NSMBULakitu.webp").convert_alpha()
        # Resize at 80x80 pixels
        self.image = py.transform.scale(original_image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 150  # Position initiale x
        self.rect.y = 150  # Position initiale y