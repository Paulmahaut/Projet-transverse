import pygame as py

class Character(py.sprite.Sprite):

    def __init__(self):
        self.square = py.Surface((20,20))
        self.rect = self.square.get_rect()
        self.rect.x = 100
        self.rect.y = 100
#Appliquer le comment on appelle ça le carré créer pour le personnage, que le personnage apparaisse dans lma fenêtre
