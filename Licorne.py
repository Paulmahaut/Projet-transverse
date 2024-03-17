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
        
        self.current_health = 500 # Valeur initial de la barre de vie
        self.maximum_health = 1000 # Valeur maximum de la barre de vie
        self.health_bar_lenght = 400 # Longeur maximal en pixel de la barre de vie
        self.health_ratio = self.maximum_health / self.health_bar_lenght # Ratio utiliser pour remplir la barre de vie
    
    def get_damage(self,amount):
        if self.current_health > 0:
            self.current_health -= amount # Baisse la valeur de la barre de vie de X 
        if self.current_health <= 0:
            self.current_health =0 # Eviter que la valeur de la barre de vie soit inférieur à 0
    
    def get_health(self,amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount # Augmente la valeur de la barre de vie de X
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health # Evite que la valeur de labarre de vie dépasse le maximum
    
    def character_health(self):
        pygame.draw.rect(screen, (255,0,0), (10,10,self.current_health/self.health_ratio,25)) # Rectangle de la barre de vie
        pygame.draw.rect(screen, (255,255,255), (10,10,self.health_bar_lenght,25),4) # Bordure de la barre de vie

    def update(self):
        self.basic_health()
        

        self.group_projectil = py.sprite.Group()
    
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
