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
        # Check for collisions with platforms
        collisions = py.sprite.spritecollide(self, self.game.group_platforms, False)
        for platform in collisions:
            # Adjust player's position to be just above the platform
            self.rect.bottom = platform.rect.top
            # Reset jump state and velocity
            self.jump_state = False
            self.jump_vel = 20
                      
    def launch_projectile(self):
        # Create a projectile and add it to group_projectile
        keys_pressed = py.key.get_pressed()
        if keys_pressed[py.K_SPACE] and not self.space_pressed_last_frame:
            self.group_projectile.add(Projectil(self))
        self.space_pressed_last_frame = keys_pressed[py.K_SPACE]  # Update space_pressed_last_frame

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
            self.kill() # kill the projectil when it's out of the window (to avoid killing the commin enemies)