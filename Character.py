#Ici tout ce qui concerne la licorne
import pygame as py
from var import *

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
        self.flip = False

        self.velocity = 5
        self.attack = 10
        self.jump_vel = 22
        self.jump_state = False

        # Health and score
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

    def jump(self):
        self.rect.y-=self.jump_vel
        self.jump_vel-=1
        if self.jump_vel <-20:
            self.jump_state = False
            self.jump_vel = 20
            
    def move(self):
        #dx = 0
        #dy = 0

        keys_pressed = py.key.get_pressed()

        # move to the left
        if keys_pressed[py.K_LEFT] and self.rect.x >10:
            # collision check with enemy
            if not self.game.check_collision(self, self.game.group_enemy):
               #dx = -self.velocity
               self.rect.x -=self.velocity
               self.flip = True # to flip the image
            if self.rect.x <= x_init and self.game.screen_scroll<0:
                self.game.direction = 1
                self.game.scroll()# move the screen 

        # move to the right
        if keys_pressed[py.K_RIGHT] and self.rect.x<50000 :
            # collision check with enemy
            if not self.game.check_collision(self, self.game.group_enemy):
               #dx = self.velocity
               self.rect.x +=self.velocity
               self.flip = False
            if self.rect.x >= WIDTH - SCROLL_LIM :
                self.game.direction = 0
                self.game.scroll()# move the screen

        # player jumps if key up is pressed    
        if keys_pressed[py.K_UP]:
            self.jump_state = True
        if self.jump_state :
            self.jump()
        
        # reset screen_scroll if it's biggier than the width of the screen
        if abs(self.game.screen_scroll) > WIDTH : 
            self.game.screen_scroll = 0 
  
        for platform in self.game.group_platforms:
            # check collision between player and platform
             if self.game.check_collision(self, self.game.group_platforms):
                # is the player higher than the platform 
                if self.rect.y < platform.rect.top  and self.jump_vel <0: 
                    # position at on the platform
                    self.jump_vel = 0
                
    def jump(self):        
        self.rect.y-=self.jump_vel
        self.jump_vel-=1
        if self.jump_vel <-22:
            self.jump_state = False
            self.jump_vel = 22

    def launch_projectil(self):
        # create a projectil and add it to group_projectil
        self.group_projectil.add(Projectil(self))

class Projectil(py.sprite.Sprite):

    def __init__(self, player):
        super(Projectil, self).__init__() 
        self.player = player
        self.velocity = 20
        rainbow_image = py.image.load("images/rainbow.png").convert_alpha()
        self.image = py.transform.scale(rainbow_image, (20, 10))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x +32
        self.rect.y = player.rect.y +32

    def move(self):
        self.rect.x+= self.velocity
        for enemy in self.player.game.check_collision(self, self.player.game.group_enemy) :
            enemy.get_damage(self.player.attack)
            self.kill() # kill the projectil when it collide with the enemy

        if self.rect.x > WIDTH :
            self.kill() # kill the projectil when it'sout of the window (to avoid killing the commin enemies)