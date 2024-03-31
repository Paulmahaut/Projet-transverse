#Ici tout ce qui concerne la licorne
import pygame as py
from var import *

class Character(py.sprite.Sprite):

    def __init__(self, game):
        super(Character, self).__init__()  # Initialise la classe parente Sprite
        self.game = game
        # Load the image
        original_image = py.image.load("playerlicorne.png").convert_alpha()
        # Resize at 80x80 pixels
        self.image = py.transform.scale(original_image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x_init  # Position initiale x
        self.rect.y = y_init  # Position initiale y
        self.group_projectil = py.sprite.Group()

        self.velocity = 5
        self.jump_vel = 20
        self.jump_state = False
        self.current_health = 1000 # Valeur initial de la barre de vie
        self.maximum_health = 1000 # Valeur maximum de la barre de vie
        self.health_bar_length = 200 # Longeur maximal en pixel de la barre de vie
        self.health_ratio = self.maximum_health / self.health_bar_length # Ratio utiliser pour remplir la barre de vie
        self.score = 0
    #--------------------------------------------
    def get_damage(self,amount):
        if self.current_health > 0:
            self.current_health -= amount # Baisse la valeur de la barre de vie de X 
        #if self.current_health <= 0:
            #self.current_health =0 # Eviter que la valeur de la barre de vie soit inférieur à 0
    
   #def get_health(self,amount):
        #if self.current_health < self.maximum_health:
            #self.current_health += amount # Augmente la valeur de la barre de vie de X
        #if self.current_health >= self.maximum_health:
            #self.current_health = self.maximum_health # Evite que la valeur de labarre de vie dépasse le maximum
    
    def update_health_bar(self, surface):
        screen_width, screen_height = surface.get_size()
        # Position et dimensions de la barre de vie
        bar_width = self.health_bar_length
        bar_height = 10  # Hauteur de la barre de vie
        x_position = screen_width - bar_width - 10  # 10 pixels de marge du bord droit
        y_position = 10  # 10 pixels de marge du haut

        # Dessiner la barre de vie
        py.draw.rect(surface, change_color(self.current_health), (self.rect.x, self.rect.y - 20, self.current_health / self.health_ratio, 10))
        py.draw.rect(surface, (255, 255, 255), (self.rect.x, self.rect.y - 20, self.health_bar_length, 10), 2)
        
    #-------------------------------------------------------
    
    def move_rigth(self):
        #self.rect.x+=self.velocity
        if not self.game.check_collision(self, self.game.group_enemy):
            self.rect.x+=self.velocity
        
    def move_left(self):
        self.rect.x-=self.velocity
        

    def jump(self):
        self.rect.y-=self.jump_vel
        self.jump_vel-=1
        if self.jump_vel <-20:
            self.jump_state = False
            self.jump_vel = 20
                      
    def launch_projectil(self):
        # create a projectil and add it to group_projectil
        self.group_projectil.add(Projectil(self))


class Projectil(py.sprite.Sprite):

    def __init__(self, player):
        super(Projectil, self).__init__() 
        self.player = player
        self.velocity = 20
        rainbow_image = py.image.load("rainbow.png").convert_alpha()
        self.image = py.transform.scale(rainbow_image, (20, 10))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x +32
        self.rect.y = player.rect.y +32

    def move(self):
        self.rect.x+= self.velocity
        for enemy in self.player.game.check_collision(self, self.player.game.group_enemy) :
            enemy.get_damage(30)
            self.kill() # kill the projectil when it collide with the enemy

        if self.rect.x > WIDTH :
            self.kill() # kill the projectil when it'sout of the window (to avoid killing the commin enemies)