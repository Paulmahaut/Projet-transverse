import pygame as py
from Ennemy import *
from Licorne import *

# INSTANCES
player = Character()
# put the player in a group in order to compare it with enemies for collision
group_player = py.sprite.Group()
group_player.add(player)

enemy = Enemy(group_player)
# gather all enemies in one group
group_enemy = py.sprite.Group()
group_enemy.add(enemy)

projectil = Projectil(player)



