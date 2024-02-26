import os
from functions import *
import pygame as py
from sys import exit

COLOR={'lightbleu':(240,248,255), 
       "almond":(240,255,240), 
       "lavander": (230,230,250), 
       "gray":(119,136,153),
       "sandy": (244,164,96)}

py.init()
clock = py.time.Clock()
screen = py.display.set_mode((1600,1000))
py.display.set_caption('Game')
screamer=py.USEREVENT+1
py.time.set_timer(screamer, 10000)
# Background design
#background = py.Surface((600,600))
#background.fill(COLOR["gray"])

#background unicorn
im=py.image.load("Backgroundunicorn.png")
test=py.image.load("screamer.jpg")
player = Character()
image_display_start = None
special_image = py.transform.scale(test, (300, 300))
#sound
song = py.mixer.Sound("tqt.mp3")

while True:
    current_time = py.time.get_ticks()
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
        elif event.type==screamer:
                        # Marquer le début de l'affichage de l'image
            image_display_start = current_time
    
    if image_display_start:
        if current_time - image_display_start <= 1000:  # 100 ms = 1/10 de seconde
            screen.blit(special_image, (900, 900))  
        else:
            image_display_start = None  # Réinitialiser pour le prochain affichage
    song.play()
    keys_pressed = py.key.get_pressed()

    if keys_pressed[py.K_UP] and player.rect.y>0:
        player.rect.y -= 5
    if keys_pressed[py.K_DOWN] and player.rect.y< 920 :
        player.rect.y += 5
    if keys_pressed[py.K_LEFT] and player.rect.x>0:
        player.rect.x -= 5
    if keys_pressed[py.K_RIGHT] and player.rect.x<1520 :
        player.rect.x += 5

    
    screen.blit(im, (0,0)) #remplacer im par background si problèmes
    screen.blit(player.image, player.rect)
    py.display.update()
    clock.tick(60)
    
