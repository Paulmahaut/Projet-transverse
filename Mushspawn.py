import pygame as py
import random

class Mushspawn(py.sprite.Sprite):
    def __init__(self):  
        super(Mushspawn, self).__init__()       
        original_image = py.image.load("NSMBULakitu.webp").convert_alpha()
        self.image = py.transform.scale(original_image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.velocity = 10
        self.mushroom_group = py.sprite.Group()

    def drop_mushroom(self):
        mushroom_image = py.image.load("images/Mushroom.png").convert_alpha()
        mushroom_rect = mushroom_image.get_rect()
        mushroom_rect.x = self.rect.x
        mushroom_rect.y = self.rect.y + self.rect.height
        
        # Create a new sprite for the mushroom
        mushroom_sprite = py.sprite.Sprite()
        mushroom_sprite.image = mushroom_image
        mushroom_sprite.rect = mushroom_rect

        # Ajouter le champignon au groupe de champignons de la classe
        self.mushroom_group.add(mushroom_sprite)

    def move(self):
        self.rect.x -= self.velocity
