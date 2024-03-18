#Ici tout ce qui concerne la licorne
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
        self.group_projectil = py.sprite.Group()
        
        self.current_health = 500 # Valeur initial de la barre de vie
        self.maximum_health = 1000 # Valeur maximum de la barre de vie
        self.health_bar_lenght = 400 # Longeur maximal en pixel de la barre de vie
        self.health_ratio = self.maximum_health / self.health_bar_lenght # Ratio utiliser pour remplir la barre de vie
        self.current_health_2 = self.current_health/self.health_ratio

    #--------------------------------------------
    #def get_damage(self,amount):
        #if self.current_health > 0:
            #self.current_health -= amount # Baisse la valeur de la barre de vie de X 
        #if self.current_health <= 0:
            #self.current_health =0 # Eviter que la valeur de la barre de vie soit inférieur à 0
    
    #def get_health(self,amount):
        #if self.current_health < self.maximum_health:
            #self.current_health += amount # Augmente la valeur de la barre de vie de X
        #if self.current_health >= self.maximum_health:
            #self.current_health = self.maximum_health # Evite que la valeur de labarre de vie dépasse le maximum
    
    #def update(self):
        #self.current_health()
        
    #-------------------------------------------------------
        
    def launch_projectile(self):
        self.group_projectil.add(Projectil(self))


class Projectil(py.sprite.Sprite):

    def __init__(self, player):
        super(Projectil, self).__init__() 

        self.velocity = 5
        rainbow_image = py.image.load("rainbow.png").convert_alpha()
        self.image = py.transform.scale(rainbow_image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x +20
        self.rect.y = player.rect.y +20

    def move(self):
        self.rect.x+=self.velocity
