#Ici se trouve tout ce qui est lié à l'ennemi
import pygame as py


class Enemy(py.sprite.Sprite):

    def __init__(self, group_player):
        super(Enemy, self).__init__()  # Initialise la classe parente Sprite

        tank_image = py.image.load("tank.png").convert_alpha()
        self.image = py.transform.scale(tank_image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 900  # Position initiale x
        self.rect.y = 400  # Position initiale y
    
    def move(self,group_player):
    # collision check
        if not py.sprite.spritecollide(self, group_player,False,  py.sprite.collide_mask):
            self.rect.x-=1

import math
import random
import time

class Tank_project: #projectiles du Tank 
    def __init__(self):
        self.angle = 0
        self.force = 0
        Tank_project_image= py.image.load("Tank_proje.png")

    def throw_projectile(self): #lancer les projectiles avec un angle variable choisit aleatoirement
        self.angle = random.uniform(0, 90)  
        self.force = random.uniform(10, 50) 
          #je sais pas trop ce que ca fait je vais verifier apres mais c'est cense etre la trajectoire
        time_of_flight = (2 * self.force * math.sin(math.radians(self.angle))) / 9.8
        horizontal_distance = self.force * math.cos(math.radians(self.angle)) * time_of_flight
        
    
Tank= Tank_project()

# pour que ca continue l'action automatiquement
while True:
    Tank.throw_projectile()
    time.sleep(random.randint(0,10)) #pour qu'il y'ait un delai entre les lancers de projectiles





