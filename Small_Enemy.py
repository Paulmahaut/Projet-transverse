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
        explosion = py.image.load("images/explosion.png").convert_alpha()
        self.explose = py.transform.scale(explosion, (100, 100))

        self.rect.x = 2000 + random.randint(0,700)  # Position initiale x
        self.rect.y = 470  # Position initiale y
        self.velocity = 4
        self.initial_health = 1
        self.attack = 200
        self.current_health = 1 # Valeur de la barre de vie
        #--------------------------------------------
    def get_damage(self,amount):
        if self.current_health > 0:
            self.current_health -= amount # Baisse la valeur de la barre de vie de X 
            self.game.player.score +=200
        elif self.current_health<=0:
            self.replace()

    def blast(self):
        self.game.screen.blit(self.explose,(self.rect.x, self.rect.y))
        #self.game.explosion_sound.play() # ne se déclanche pas

    def replace(self):
        self.blast()
        self.rect.x = 2000 + random.randint(0,500) # moved as a new enemy
        self.current_health = self.initial_health
                 
        
    def move(self):
    # collision check
        if not self.game.check_collision(self, self.game.group_player):
            self.rect.x-= self.velocity
        else :
            self.game.player.get_damage(self.attack)
            self.current_health = 0
    
        if self.rect.x <-300 or self.current_health == 0:
            self.replace() # if the enemy step out of the screen we replace it 