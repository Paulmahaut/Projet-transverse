import os
from Enemy import *
from Licorne import *
import pygame as py
from sys import exit
import random
 
COLOR={'lightbleu':(240,248,255), 
       "almond":(240,255,240), 
       "lavander": (230,230,250), 
       "gray":(119,136,153),
       "sandy": (244,164,96)}

# VARIABLES
LOOSE = False

random.seed()
py.init()
clock = py.time.Clock()
current_time = py.time.get_ticks()

screen = py.display.set_mode((1000,700))
py.display.set_caption('Game')
# à modifier
screamer=py.USEREVENT+1
py.time.set_timer(screamer, 10000)

# Background design
background = py.Surface((1000,700))
background.fill(COLOR["gray"])

#background unicorn
im=py.image.load("Backgroundunicorn.png")
test=py.image.load("screamer.jpg")
explosion=py.image.load("explosion.png")
explosion = py.transform.scale(explosion, (200, 200))
image_display_start = None
special_image = py.transform.scale(test, (300, 300))

#sound
song = py.mixer.Sound("tqt.mp3")
explosion_sound = py.mixer.Sound("Explosion sound.mp3")

#Chan1=py.mixer.Channel(0)
#Chan2=py.mixer.Channel(1)

# INSTANCES
player = Character()
# put the player in a group in order to compare it with enemies for collision
group_player = py.sprite.Group()
group_player.add(player)

enemy = Enemy(group_player)
# gather all enemies in one group
group_enemy = py.sprite.Group()
group_enemy.add(enemy)


#TANK_SHOOT = py.USEREVENT + 2
#py.time.set_timer(TANK_SHOOT, 10000)  # Exemple : Lance un projectile toutes les 10 secondes

TANK_SHOOT =0
jump = False
projectil = Projectil(player)
tank_proj = Tank_project(enemy)

while True:

    # DISPLAY
    #screen.blit(im, (0,0)) #remplacer im par background si problèmes
    screen.blit(background, (0,0))
    screen.blit(player.image, player.rect)
    player.update_health_bar(screen)
    enemy.update_health_bar(screen)

    player.update() #Pour mettre à jour chaque frame la barre de vie afin de pouvoir la changer 

    # Move projectils and enemies in groups
    for enemy in group_enemy:
        enemy.move(group_player)

    for projectile in player.group_projectil:
        projectile.move()
    
    for projectile_tank in enemy.group_projectil:
        projectile_tank.throw_projectile()
    

    # display all enmies and projectiles groups
    group_enemy.draw(screen)
    player.group_projectil.draw(screen)
    enemy.group_projectil.draw(screen)

    

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
        
        
        # à modifeier avec LOOSE
        elif event.type==screamer:
                        # Marquer le début de l'affichage de l'image
            image_display_start = current_time


    if image_display_start:
        if current_time - image_display_start <= 1000:  # 100 ms = 1/10 de seconde
            screen.blit(special_image, (900, 900))  
        else:
            image_display_start = None  # Réinitialiser pour le prochain affichage
    
   # song.play()        
        
            
    # KEYBOARD
    keys_pressed = py.key.get_pressed()

    #if keys_pressed[py.K_UP] and player.rect.y>0:
        #player.rect.y -= 5
    #if keys_pressed[py.K_DOWN] and player.rect.y< 920 :
        #player.rect.y += 5
    if keys_pressed[py.K_LEFT] and player.rect.x>0:
        player.rect.x -= 5
    if keys_pressed[py.K_RIGHT] and player.rect.x<1520 :
        # collision check 
        if not py.sprite.spritecollide(player,group_enemy, False, py.sprite.collide_mask): 
            player.rect.x += 5
    if keys_pressed[py.K_SPACE]:
        player.launch_projectile()
        
    if not jump and keys_pressed[py.K_UP]:
        jump = True
    if jump:
        jump = player.jump()

    if keys_pressed[py.K_a]:
        enemy.throw_projectile()
    
    TANK_SHOOT = random.randint(0,100)
    #event déclenchant la fonction throw proj
    if TANK_SHOOT%10 ==0 and enemy.current_health >0:
        enemy.throw_projectile()
        
        
    for projectile in enemy.group_projectil:
    # Vérifie si le projectile entre en collision avec la licorne
        if py.sprite.collide_rect(projectile, player):
            # Gérer la collision ici (par exemple, infliger des dégâts)
            player.get_damage(30)
            projectile.kill()  # Supprime le projectile après la collision 
    
    for projectile in player.group_projectil:
    # Vérifie si le projectile entre en collision avec la licorne
        if py.sprite.collide_rect(projectile, enemy):
            # Gérer la collision ici (par exemple, infliger des dégâts)
            enemy.get_damage(30) 
            projectile.kill()  # Supprime le projectile après la collision 
    
    if enemy.current_health <=0:
        enemy.kill()
        screen.blit(explosion,(enemy.rect.x, enemy.rect.y))
        explosion_sound.play()
        
        
    py.display.update()
    clock.tick(60)
                                
