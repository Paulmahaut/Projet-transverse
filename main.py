import os
from functions import *
import pygame as py
from sys import exit

COLOR={'lightbleu':(240,248,255), 
       "almond":(240,255,240), 
       "lavander": (230,230,250), 
       "gray":(119,136,153),
       "sandy": (244,164,96)}

# VARIABLES
LOOSE = False

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
image_display_start = None
special_image = py.transform.scale(test, (300, 300))

#sound
song = py.mixer.Sound("tqt.mp3")

# INSTANCES
player = Character()
# put the player in a group in order to compare it with enemies for collision
group_player = py.sprite.Group()
group_player.add(player)

enemy = Enemy(group_player)
# gather all enemies in one group
group_enemy = py.sprite.Group()
group_enemy.add(enemy)


while True:

    # DISPLAY
    #screen.blit(im, (0,0)) #remplacer im par background si problèmes
    screen.blit(background, (0,0))
    screen.blit(player.image, player.rect)

    for enemy in group_enemy:
        enemy.move(group_player)
    
    # display all enmies in the group
    group_enemy.draw(screen)
    
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
    
    #song.play()
            
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

    py.display.update()
    clock.tick(60)
    
