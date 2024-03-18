#Ici se trouve tout ce qui est lié à l'ennemi
import pygame as py
import math
import random
import time

class Enemy(py.sprite.Sprite):

    def __init__(self, group_player):
        super(Enemy, self).__init__()  # Initialise la classe parente Sprite

        tank_image = py.image.load("tank.png").convert_alpha()
        self.image = py.transform.scale(tank_image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 900  # Position initiale x
        self.rect.y = 400  # Position initiale y
        self.group_projectil = py.sprite.Group()
    
    def move(self,group_player):
    # collision check
        if not py.sprite.spritecollide(self, group_player,False,  py.sprite.collide_mask):
            self.rect.x-=1

    def launch_projectile(self):
        self.group_projectil.add(Tank_project(self))



class Tank_project(py.sprite.Sprite): #projectiles du Tank 

    def __init__(self, enemy):
        super(Tank_project, self).__init__() 

        self.angle = 0
        self.force = 0
        
        self.velocity = 2
        tank_project_image= py.image.load("Tank_proje.png")
        self.image = py.transform.scale(tank_project_image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = enemy.rect.x
        self.rect.y = enemy.rect.y +60    

    def throw_projectile(self): #lancer les projectiles avec un angle variable choisit aleatoirement
        #self.angle = random.uniform(0, 90)  
        #self.force = random.uniform(10, 50) 
        self.rect.x-=self.velocity
        #je sais pas trop ce que ca fait je vais verifier apres mais c'est cense etre la trajectoire
        #time_of_flight = (2 * self.force * math.sin(math.radians(self.angle))) / 9.8
        #horizontal_distance = self.force * math.cos(math.radians(self.angle)) * time_of_flight
           


# pour que ca continue l'action automatiquement
'''
while True:
    Tank.throw_projectile()
    time.sleep(random.randint(0,10)) #pour qu'il y'ait un delai entre les lancers de projectiles
'''


