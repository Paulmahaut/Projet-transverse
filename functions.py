import pygame as py
class Character(py.sprite.Sprite):

    def __init__(self):
        super(Character, self).__init__()  # Initialise la classe parente Sprite
        # Charger l'image originale
        original_image = py.image.load("playerlicorne.png").convert_alpha()
        # Redimensionner l'image à 80x80 pixels
        self.image = py.transform.scale(original_image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 100  # Position initiale x
        self.rect.y = 430  # Position initiale y
    

class Enemy(py.sprite.Sprite):

    def __init__(self, group_player):
        super(Enemy, self).__init__()  # Initialise la classe parente Sprite

        tank_image = py.image.load("tank.png").convert_alpha()
        self.image = py.transform.scale(tank_image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 900  # Position initiale x
        self.rect.y = 400  # Position initiale y

    def move(self,group_player):
        # collision check
        if not py.sprite.spritecollide(self, group_player,False,  py.sprite.collide_mask):
            self.rect.x-=1

class Projectil(py.sprite.Sprite):
    def __init__(self, player):
        super(Projectil, self).__init__() 

        self.velocity = 5
        rainbow_image = py.image.load("rainbow.png").convert_alpha()
        self.image = py.transform.scale(rainbow_image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x 
        self.rect.y = player.rect.y
    
    def move(self):
        self.rect.x+=self.velocity

