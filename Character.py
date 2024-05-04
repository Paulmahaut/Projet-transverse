#Ici tout ce qui concerne la licorne
import pygame as py
from var import *
import math
from trajectory import *

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

        self.group_projectil = py.sprite.Group()

        self.velocity = 5
        self.attack = 10
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
        if not self.game.check_collision(self, self.game.group_enemy):
            self.rect.x+=self.velocity
        
    def move_left(self):
        if not self.game.check_collision(self, self.game.group_enemy):
            self.rect.x-=self.velocity
        

    def jump(self):
        self.rect.y-=self.jump_vel
        self.jump_vel-=1
        if self.jump_vel <-20:
            self.jump_state = False
            self.jump_vel = 20
                      
    def launch_projectil(self):
        # create a projectil and add it to group_projectil
        self.group_projectil.add(Projectil(self, ))
    


class Projectil(py.sprite.Sprite):

    def __init__(self, player,proj, theta):
        super(Projectil, self).__init__() 
        self.player = player
        self.proj = proj
        self.velocity = 20
        rainbow_image = py.image.load("images/rainbow.png").convert_alpha()
        self.image = py.transform.scale(rainbow_image, (20, 10))
        self.rect = self.image.get_rect()                                      
        self.rect.x = player.rect.x +32
        self.rect.y = player.rect.y +32
        self.origin = (self.rect.x, self.rect.y)
        self.theta = toradian(abs(theta))
        self.ch = 0
        self.dx = 2
        self.teta = -30
        self.f = self.trajectory()
        self.range = self.x + abs(self.range())
        self.path = []

    def launch_projectil_traj(self):
        
        if -90 < self.player.theta <= 0:
        #projectile = self.Projectil(proj, theta)
        #self.player.projectile_group.add(projectile)
            self.player.launch_projectil()            

    def move(self):
        self.rect.x+= self.velocity
        for enemy in self.proj.game.check_collision(self, self.proj.game.group_enemy) :
            enemy.get_damage(self.proj.attack)
            self.kill() # kill the projectil when it collide with the enemy

        if self.rect.x > WIDTH :
            self.kill() # kill the projectil when it'sout of the window (to avoid killing the commin enemies)

    def timeofflight(self):
        return round ((2*self.proj*math.sin(self.theta))/g, 2)
    
    def range(self):
        range1 = ((self.proj**2)*2*math.sin(self.theta)*math.cos(self.theta))/g
        return round(range1,2)
    
    def maxheight(self):
        h = ((self.pproj ** 2) * (math.sin(self.theta)) ** 2) / (2 * g)
        return round(h, 2)
    
    def trajectory(self):
        return round(g /  (2 * (self.proj ** 2) * (math.cos(self.theta) ** 2)), 4)
    
    def positionprojectile(self, x):
        return x * math.tan(self.theta) - self.f * x ** 2
    
    def update(self):
        if self.rect.x >= self.range:
            self.dx = 0
        self.rect.x += self.dx
        self.ch = self.positionprojectile(self.origin[0] - self.proj.rect[0])

        self.path.append((self.origin[0], self.origin[1]-abs(self.ch)))
        self.path = self.path[-50:]

    









