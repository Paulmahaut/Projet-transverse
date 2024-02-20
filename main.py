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
screen = py.display.set_mode((600,600))
py.display.set_caption('Game')

# Background design
background = py.Surface((600,600))
background.fill(COLOR["gray"])

player = Character()

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
    
    keys_pressed = py.key.get_pressed()

    if keys_pressed[py.K_UP] and player.rect.y>0:
        player.rect.y -= 5
    if keys_pressed[py.K_DOWN] and player.rect.y< 580 :
        player.rect.y += 5
    if keys_pressed[py.K_LEFT] and player.rect.x>0:
        player.rect.x -= 5
    if keys_pressed[py.K_RIGHT] and player.rect.x<580 :
        player.rect.x += 5

    
    screen.blit(background, (0,0))
    screen.blit(player.square, player.rect)
    py.display.update()
    clock.tick(60)

