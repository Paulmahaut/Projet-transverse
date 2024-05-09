#Ici tout ce qui concerne la licorne
import pygame as py
from var import *
from math import *
from trajectory import *
import random

class Character(py.sprite.Sprite):

    def __init__(self, game):
        super(Character, self).__init__()  # Initialise la classe parente Sprite
        self.game = game
        # Load the image
        original_image = py.image.load("images/playerlicorne.png").convert_alpha()
        # Resize at 80x80 pixels
        self.image = py.transform.scale(original_image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x_init  # Position initiale x
        self.rect.y = y_init  # Position initiale y
        self.flip = False
        self.sign = 1
        self.nul = 0

        self.group_projectil = py.sprite.Group()

        self.velocity = 5
        self.attack = 200
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

    def update_health_bar(self, surface):
        # Dessiner la barre de vie
        py.draw.rect(surface, change_color(self.current_health), (self.rect.x, self.rect.y - 20, self.current_health / self.health_ratio, 10))
        py.draw.rect(surface, (255, 255, 255), (self.rect.x, self.rect.y - 20, self.health_bar_length, 10), 2)
        
    #-------------------------------------------------------
    
    def move_rigth(self):
        if not self.game.check_collision(self, self.game.group_enemy):
            self.rect.x+=self.velocity

            # to flip the image and the shoot
            self.flip = False 
            self.sign = 1
            self.nul = 0
        
    def move_left(self):
        if not self.game.check_collision(self, self.game.group_enemy):
            self.rect.x-=self.velocity

            # to flip the image and the shoot
            self.flip = True 
            self.sign = -1
            self.nul = 1
        

    def jump(self):
        self.rect.y-=self.jump_vel
        self.jump_vel-=1
        if self.jump_vel <-20:
            self.jump_state = False
            self.jump_vel = 20
                      
    def launch_projectil(self, theta, origin_proj):
        # create a projectil and add it to group_projectil
        self.group_projectil.add(Projectil(self, v_init, theta, origin_proj))
    
    def super_attack(self):
        pass
        

class Projectil(py.sprite.Sprite):

    def __init__(self, player, v_init, theta, origin_proj):
        super(Projectil, self).__init__() 
        self.player = player
        self.v_init= v_init
        self.velocity = 20

        # coord projectil
        self.origin_proj=origin_proj
        self.x, self.y = self.origin_proj

        # image projectil
        rainbow_image = py.image.load("images/rainbow.png").convert_alpha()
        self.image = py.transform.scale(rainbow_image, (20, 10))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.origin_proj

        self.theta = to_radian(abs(theta))
        self.ch = 0
        self.dx = 4
        self.dy = 0
        self.sign = 1

        self.f = self.slope_trajectory()
        self.max_range = self.rect.x + abs(self.max_range())
        self.path = []          

    def max_range(self):
        range1 = (((self.v_init**2)*2*sin(self.theta)*cos(self.theta))/g )
        return round(range1,2)
    
    def max_height(self):
        h = ((self.v_init** 2) * (sin(self.theta)) ** 2) / (2 * g)
        return round(h, 2)
    
    def slope_trajectory(self):
        # slope of the trajectory equation
        return round((g /  (2 * (self.v_init** 2) * (cos(self.theta) ** 2))), 4)
    
    def position_projectile(self, x):
        # trajectory equation
        return x * tan(self.theta) - self.f * x ** 2 

    def update(self):
        if self.x >= self.max_range :
            self.sign = -1
        self.x += self.dx
        self.ch = self.position_projectile(self.x - self.origin_proj[0])

        self.path.append((self.x, self.y- self.sign * abs(self.ch)))
        self.path = self.path[-50:]

        # displlay projectil
        self.player.game.screen.blit(self.image, self.path[-1])
        for pos in self.path[:-1:5]:
            py.draw.circle(self.player.game.screen, COLOR['white'], pos, 1)

        # update rect coord to compare sprites 
        self.rect.x, self.rect.y = self.x, self.y- self.sign * abs(self.ch)

        # kill the projectil when it collides with the enemy
        for enemy in self.player.game.check_collision(self, self.player.game.group_enemy) :
            enemy.get_damage(self.player.attack)
            self.kill() 

        # delete the projectil if it's out of the window or near to the groud
        if self.rect.x > WIDTH or self.rect.y >= y_init +100:
                self.kill()












