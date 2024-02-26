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

# Background design
#background = py.Surface((600,600))
#background.fill(COLOR["gray"])

#background unicorn
im=py.image.load("Backgroundunicorn.png")

player = Character()


#sound
song = py.mixer.Sound("tqt.mp3")

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
    
    song.play()
    keys_pressed = py.key.get_pressed()

    if keys_pressed[py.K_UP] and player.rect.y>0:
        player.rect.y -= 5
    if keys_pressed[py.K_DOWN] and player.rect.y< 980 :
        player.rect.y += 5
    if keys_pressed[py.K_LEFT] and player.rect.x>0:
        player.rect.x -= 5
    if keys_pressed[py.K_RIGHT] and player.rect.x<1580 :
        player.rect.x += 5

    
    screen.blit(im, (0,0)) #remplacer im par background si problèmes
    screen.blit(player.square, player.rect)
    py.display.update()
    clock.tick(60)
    
