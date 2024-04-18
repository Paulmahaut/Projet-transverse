import pygame as py
import random
from var import*
import math

class Mushspawn(py.sprite.Sprite):
    def __init__(self):  
        super(Mushspawn, self).__init__()  # Initialise la classe parente Sprite       
        # Load the image
        original_image = py.image.load("NSMBULakitu.webp").convert_alpha()
        # Resize at 80x80 pixels
        self.image = py.transform.scale(original_image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 200  # Position initiale x
        self.Groupe_Mush = py.sprite.Group() 
        self.velocity = 25
        
    def throw_projectile(self): 
        self.Groupe_Mush.add(Mush_project(self)) 
    
    def move(self):
       if self.rect.x < WIDTH:
                self.rect.x+= self.velocity
       else:
            if self.rect.x > WIDTH:
                self.rect.x +- self.velocity



    
class Mush_project(py.sprite.Sprite): #projectiles du lakitu
    def __init__(self, Mushspawn):
        super(Mush_project, self).__init__() 
        self.Mushspawn = Mushspawn
        self.angle = 0
        self.force = 0
        
        self.velocity = 5
        Mush_project_image= py.image.load("images/Mushroom.png")
        self.image = py.transform.scale(Mush_project_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = Mushspawn.rect.x 
        self.rect.y = Mushspawn.rect.y + 60    
       
    def move(self): #lancer les projectiles avec un angle variable choisit aleatoirement
        #self.angle = random.uniform(0, 90)  
        #self.force = random.uniform(10, 50)
        
        self.rect.y+=self.velocity
        if self.rect.x > WIDTH :
            self.kill()       
        