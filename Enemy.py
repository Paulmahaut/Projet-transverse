#Ici se trouve tout ce qui est lié à l'ennemi
import pygame as py
import math
import random
from var import *

class Enemy(py.sprite.Sprite):

    def __init__(self, game):
        super(Enemy, self).__init__()  # Initialise la classe parente Sprite

        self.game = game
        tank_image = py.image.load(ENEMY[self.game.current_level]).convert_alpha()
        self.image = py.transform.scale(tank_image, (150, 150))
        self.rect = self.image.get_rect()
        explosion = py.image.load("images/explosion.png").convert_alpha()
        self.explose = py.transform.scale(explosion, (150, 150))

        self.rect.x = 1000 + random.randint(0,700)  # Position initiale x
        self.rect.y = 400  # Position initiale y
        self.velocity = 1
        self.attack = 10
        self.initial_health = 1000
        self.current_health = 1000 # Valeur initial de la barre de vie
        self.maximum_health = 1000 # Valeur maximum de la barre de vie
        self.health_bar_length = 200 # Longeur maximal en pixel de la barre de vie
        self.health_ratio = self.maximum_health / self.health_bar_length # Ratio utilisé pour remplir la barre de vie

        self.group_projectil = py.sprite.Group()
        #--------------------------------------------
    def get_damage(self,amount):
        if self.current_health > 0:
            self.current_health -= amount # Baisse la valeur de la barre de vie de X 
            self.game.player.score +=30
        elif self.current_health<=0:
            self.replace()

    def blast(self):
        self.game.screen.blit(self.explose,(self.rect.x, self.rect.y))
        #self.game.explosion_sound.play() # ne se déclanche pas

    def replace(self):
        self.blast()
        self.rect.x = 1000 + random.randint(0,500) # moved as a new enemy
        self.current_health = self.initial_health
    
    def update_health_bar(self, surface):
        screen_width, screen_height = surface.get_size()
        # Position et dimensions de la barre de vie
        bar_width = self.health_bar_length
        bar_height = 10  # Hauteur de la barre de vie
        x_position = screen_width - bar_width - 10  # 10 pixels de marge du bord droit
        y_position = 10  # 10 pixels de marge du haut

        # Dessiner la barre de vie
        if self.current_health >=0:
            py.draw.rect(surface, change_color(self.current_health), (self.rect.x, self.rect.y - 20, self.current_health / self.health_ratio, 10))
            py.draw.rect(surface, (255, 255, 255), (self.rect.x, self.rect.y - 20, self.health_bar_length, 10), 2)
              
        
    def move(self):
    # collision check
        if not self.game.check_collision(self, self.game.group_player):
            self.rect.x-= self.velocity
        else :
            self.game.player.get_damage(10)
    
        if self.rect.x <-300:
            self.replace() # if the enemy step out of the screen we replace it 

    def throw_projectile(self):
        self.group_projectil.add(Tank_project(self))      

class Tank_project(py.sprite.Sprite): #projectiles du Tank 

    def __init__(self, enemy):
        super(Tank_project, self).__init__() 
        self.enemy = enemy
        self.angle = 0
        self.force = 0
        
        self.velocity = 17
        tank_project_image= py.image.load(ENEMY_PROJ[self.enemy.game.current_level])
        self.image = py.transform.scale(tank_project_image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = enemy.rect.x
        self.rect.y = enemy.rect.y + 60    
       
    def move(self): #lancer les projectiles avec un angle variable choisit aleatoirement
        #self.angle = random.uniform(0, 90)  
        #self.force = random.uniform(10, 50)
        
        self.rect.x-=self.velocity
        
        # if collision or not on screen the projectil is removed
        for player in self.enemy.game.check_collision(self, self.enemy.game.group_player) :
            player.get_damage(self.enemy.attack)
            self.kill()

        if self.rect.x > WIDTH :
            self.kill()
        #je sais pas trop ce que ca fait je vais verifier apres mais c'est cense etre la trajectoire
        #time_of_flight = (2 * self.force * math.sin(math.radians(self.angle))) / 9.8
        #horizontal_distance = self.force * math.cos(math.radians(self.angle)) * time_of_flight
             

# pour que ca continue l'action automatiquement
'''
while True:
    Tank.throw_projectile()
    time.sleep(random.randint(0,10)) #pour qu'il y'ait un delai entre les lancers de projectiles
'''


