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

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
        
    
    py.display.update()
    clock.tick(60)