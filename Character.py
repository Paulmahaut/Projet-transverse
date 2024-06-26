#Ici tout ce qui concerne la licorne
import pygame as py
from var import *
from math import *
from trajectory import *
import random

class Character(py.sprite.Sprite):

    def __init__(self, game):
        super(Character, self).__init__()
        self.game = game
        # Load the image
        original_image = py.image.load("images/playerlicorne2.png").convert_alpha()
        # Resize at 80x80 pixels
        self.image = py.transform.scale(original_image, (140, 80))
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
        
        self.current_health = 1000 # Initial value of health bar
        self.maximum_health = 1000 # Maximal value of health bar
        self.health_bar_length = 200
        self.health_ratio = self.maximum_health / self.health_bar_length # Ratio to fill the bar
        self.score = 0
    #--------------------------------------------
    def get_damage(self,amount):
        if amount>0 : # to make damage
            if self.current_health > 0:
                self.current_health -= amount 
        else:
            for i in range(abs(amount)):
                if self.current_health <self.maximum_health:
                    self.current_health += 1


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
                      
    def launch_projectil(self, theta, origin_proj, sign):
        # create a projectil and add it to group_projectil
        self.group_projectil.add(Projectil(self, v_init, theta, origin_proj, sign))

#https://github.com/pyGuru123/Simulations/blob/main/Projectile%20Motion/main.py 
class Projectil(py.sprite.Sprite):

    def __init__(self, player, v_init, theta, origin_proj, sign):
        super(Projectil, self).__init__() 
        self.player = player
        self.v_init= v_init
        self.velocity = 20

        # coord projectil
        self.origin_proj=origin_proj
        self.x, self.y = self.origin_proj[0], self.origin_proj[1]+90

        # image projectil
        rainbow_image = py.image.load("images/projectileunicorn.png").convert_alpha()
        self.image = py.transform.scale(rainbow_image, (30, 20))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.origin_proj
        self.angle = 1
        
        self.theta = to_radian(abs(theta))
        self.ch = 0
        self.dx = 4
        self.height_player = 90
        # to shoot to rigth or left
        self.sign = sign

        self.f = self.slope_trajectory()
        self.max_range = self.rect.x + abs(self.max_range())
        self.path = []          

    def max_range(self):
        # compute when the projectil will touch the ground
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
        return x * tan(self.theta) * self.sign - self.f * x ** 2 + self.height_player
    

    def update(self):
        self.x += self.dx * self.sign
        self.ch = self.position_projectile(self.x - self.origin_proj[0])

        self.path.append((self.x, self.y- abs(self.ch)))
        self.path = self.path[-50:]

        # display projectil
        self.player.game.screen.blit(self.image, self.path[-1])
        for pos in self.path[:-1:5]:
            py.draw.circle(self.player.game.screen, COLOR['white'], pos, 1)

        # update rect coord to compare sprites 
        self.rect.x, self.rect.y = self.x, self.y- abs(self.ch)

        # kill the projectil when it collides with the enemy and damage the enemy
        for enemy in self.player.game.check_collision(self, self.player.game.group_enemy) :
            enemy.get_damage(self.player.attack)
            self.kill() 
        
        # same for small_enemy
        for small_enemy in self.player.game.check_collision(self, self.player.game.group_small_enemy) :
            small_enemy.health = 0
            self.kill() 

        # delete the projectil if it's out of the window or near to the groud
        if self.rect.x > WIDTH or self.rect.y >= y_init +80:
                self.kill()