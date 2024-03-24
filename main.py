import os
from Enemy import *
from Licorne import *
import pygame as py
from sys import exit
import random
from var import*

random.seed()
py.init()
clock = py.time.Clock()
current_time = py.time.get_ticks()

# Window
screen = py.display.set_mode((WIDTH,HEIGHT))
py.display.set_caption('Game')

# à modifier
screamer=py.USEREVENT+1
py.time.set_timer(screamer, 10000)

# Background design
background = py.Surface((WIDTH,HEIGHT))
background.fill(COLOR["almond"])
wallpaper = py.image.load("wallpaper.jpg")
ground = py.image.load("ground2.png")
ground = py.transform.scale(ground,(WIDTH,HEIGHT))
wallpaper = py.transform.scale(wallpaper, (WIDTH, HEIGHT))

#background unicorn
im=py.image.load("Backgroundunicorn.png")
test=py.image.load("screamer.jpg")
#explosion = py.transform.scale(explosion, (200, 200))
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

player_proj = Projectil(player)
tank_proj = Tank_project(enemy)

#TANK_SHOOT = py.USEREVENT + 2
#py.time.set_timer(TANK_SHOOT, 10000)  # Exemple : Lance un projectile toutes les 10 secondes

# to move the background
def draw_bg():
    for i in range(5):
        screen.blit(wallpaper,((i * WIDTH)+screen_scroll, bg_y))

# cjange the de scroll value
# i changes in fct of the direction
def scroll(screen_scroll, i):
    player.rect.x = player.rect.x + (-1)**i * player.velocity
    screen_scroll = screen_scroll + (-1)**i * player.velocity
    enemy.rect.x = enemy.rect.x + (-1)**i * player.velocity
    return screen_scroll

""" pb when the screen moves : 
- the tank can pass its proj
- when we go back to the begining the background is messy
"""

while True:

    # DISPLAY
    #screen.blit(im, (0,0)) #remplacer im par background si problèmes
    draw_bg()

    screen.blit(player.image, player.rect)
    player.update_health_bar(screen)
    enemy.update_health_bar(screen)

    player.update() #Pour mettre à jour chaque frame la barre de vie afin de pouvoir la changer 

    # Move projectils and enemies that are in groups
    for enemy in group_enemy:
        enemy.move(group_player)

    for projectile_player in player.group_projectil:
        projectile_player.move()
    
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
        player.move_left()
        if player.rect.x <= SCROLL_LIM :
            screen_scroll = scroll(screen_scroll,0)

    if keys_pressed[py.K_RIGHT] and player.rect.x<50000 :
        # collision check 
        if not py.sprite.spritecollide(player,group_enemy, False, py.sprite.collide_mask): 
            player.move_rigth()
            if player.rect.x >= WIDTH - SCROLL_LIM :
                screen_scroll = scroll(screen_scroll,1)

    if abs(screen_scroll)> WIDTH :
        screen_scroll = 0

    if keys_pressed[py.K_SPACE]:
        player.launch_projectile()
    # player jump 
    if keys_pressed[py.K_UP]:
        player.jump_state = True
    if player.jump_state :
        player.jump()

    if keys_pressed[py.K_a]:
        enemy.throw_projectile() # to remove at the end
    
    TANK_SHOOT = random.randint(0,100)
    #event déclenchant la fonction throw proj
    if TANK_SHOOT%20 ==0 and enemy.current_health >0:
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
            
            # la collision continue qund l'enemi est mort
            #print(py.sprite.collide_rect(projectile, enemy))

    # if enemy.current_health <=0 and (enemy in group_enemy): 
    # first condition always true after the death of enemy
    # the second allows to know if the enemy still exists
        #enemy.blast()
        #group_enemy.draw(screen)
        #enemy.kill()
        #screen.blit(explosion,(enemy.rect.x, enemy.rect.y))
        #explosion_sound.play()
    
    #if player.current_health <=0:
        # message GAME OVER
        # faire une class "game manager"
        

    print("x player",player.rect.x)

    py.display.update()
    clock.tick(60)
                                
