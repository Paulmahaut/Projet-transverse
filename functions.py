import pygame as py
class Character(py.sprite.Sprite):

    def __init__(self):
        super(Character, self).__init__()  # Initialise la classe parente Sprite
        # Charger l'image originale
        original_image = py.image.load("playerlicorne.png").convert_alpha()
        # Redimensionner l'image à 80x80 pixels
        self.image = py.transform.scale(original_image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = 100  # Position initiale x
        self.rect.y = 100  # Position initiale y
    

class Enemy(py.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()  # Initialise la classe parente Sprite

        tank_image = py.image.load("tank.png").convert_alpha()
        self.image = py.transform.scale(tank_image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 900  # Position initiale x
        self.rect.y = 400  # Position initiale y

    def move(self):
        self.rect.x-=5