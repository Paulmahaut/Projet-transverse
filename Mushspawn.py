import pygame as py
import random
from var import*
import math

class Mushspawn(py.sprite.Sprite):
    def __init__(self,game):  
        self.game=game
        super(Mushspawn, self).__init__()  # Initialise la classe parente Sprite       
        # Load the image
        original_image = py.image.load("images/nuagemushroom.png").convert_alpha()
        # Resize at 80x80 pixels
        self.image = py.transform.scale(original_image, (300, 90))
        self.rect = self.image.get_rect()
        self.rect.x = -11  # Position initiale x
        self.group_mush = py.sprite.Group() 
        self.velocity = 2
        
    def throw_projectile(self): 
        self.group_mush.add(Mush_project(self)) 
    
    def move(self):
       if self.rect.x < 0:
           self.count=0
       if self.rect.x > WIDTH:
           self.count=1
       if self.count==0: 
            self.rect.x+= self.velocity
       else:
            self.rect.x -= self.velocity
            
class Mush_project(py.sprite.Sprite): #projectiles du lakit
    def __init__(self, mushspawn):
        super(Mush_project, self).__init__() 
        self.mushspawn = mushspawn
        self.angle = 0
        self.force = 0
        self.velocity = 5
        Mush_project_image= py.image.load("images/mushroompixel.png")
        self.image = py.transform.scale(Mush_project_image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = mushspawn.rect.x 
        self.rect.y = mushspawn.rect.y + 60  
    
    def move(self): #lancer les projectiles avec un angle variable choisit aleatoirement
        
        self.rect.y+=self.velocity
        if self.rect.x > WIDTH or self.rect.y > y_init+80:
            self.kill() 
            
        for player in self.mushspawn.game.check_collision(self, self.mushspawn.game.group_player) : 
            Mush_project.kill(self)
            # health bonus
            if self.mushspawn.game.player.current_health < self.mushspawn.game.player.maximum_health :
                player.get_damage(-50)
            