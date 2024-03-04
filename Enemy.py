#Ici se trouve tout ce qui est lié à l'ennemi
import pygame as py


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

#class Tank_projectil(py.sprite.sprite):
    
 #   def 





