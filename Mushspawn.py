import pygame as py
import random

class Mushspawn(py.sprite.Sprite):
    def __init__(self):  
        super(Mushspawn, self).__init__()  # Initialise la classe parente Sprite       
        # Load the image
        original_image = py.image.load("NSMBULakitu.webp").convert_alpha()
        # Resize at 80x80 pixels
        self.image = py.transform.scale(original_image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 200  # Position initiale y
         
    