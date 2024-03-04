#Ici tout ce qui concerne la licorne
import pygame as py


class Character(py.sprite.Sprite):

    def __init__(self):
        super(Character, self).__init__()  # Initialise la classe parente Sprite
        # Charger l'image originale
        original_image = py.image.load("playerlicorne.png").convert_alpha()
        # Redimensionner l'image à 80x80 pixels
        self.image = py.transform.scale(original_image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 100  # Position initiale x
        self.rect.y = 430  # Position initiale y

        self.group_projectil = py.sprite.Group()
    
    def launch_projectile(self):
        self.group_projectil.add(Projectil(self))


class Projectil(py.sprite.Sprite):

    def __init__(self, player):
        super(Projectil, self).__init__() 

        self.velocity = 5
        rainbow_image = py.image.load("rainbow.png").convert_alpha()
        self.image = py.transform.scale(rainbow_image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x +20
        self.rect.y = player.rect.y +20

    def move(self):
        self.rect.x+=self.velocity
