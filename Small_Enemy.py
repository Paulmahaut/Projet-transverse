import pygame as py
import math
import random
from var import *

class Small_Enemy(py.sprite.Sprite):

    def __init__(self, game):
        super(Small_Enemy, self).__init__()  # Initialise la classe parente Sprite

        self.game = game
        tank_image = py.image.load("images/small_enemy.png").convert_alpha()
        self.image = py.transform.scale(tank_image, (60, 50))
        self.rect = self.image.get_rect()
        explosion = py.image.load("images/explosion2.png").convert_alpha()
        self.explose = py.transform.scale(explosion, (90, 90))

        self.rect.x = 2000 + random.randint(0,700)  # Position initiale x
        self.rect.y = y_init +30  # Position initiale y
        self.velocity = 4
        self.health = 1
        self.attack = 150


    def blast(self):
        self.game.screen.blit(self.explose,(self.rect.x, self.rect.y))
        #self.game.explosion_sound.play() # ne se déclanche pas

    def replace(self):
        self.blast()
        self.rect.x = 2000 + random.randint(0,500) # moved as a new enemy
        self.health = self.health
                 
        
    def move(self):
    # collision check
        if not self.game.check_collision(self, self.game.group_player):
            self.rect.x-= self.velocity
        else :
            self.game.player.get_damage(self.attack)
            self.health = 0
    
        if self.rect.x <-300 or self.health == 0:
            self.replace() # if the enemy step out of the screen we replace it 