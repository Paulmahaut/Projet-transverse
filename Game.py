import pygame as py
import random
from sys import *
from math import *

from var import *
from Enemy import *
from Character import *


class Game :
    def __init__(self):
        py.init()
        random.seed()
        self.clock = py.time.Clock()
        #current_time = py.time.get_ticks()

        # Window
        self.screen = py.display.set_mode((WIDTH,HEIGHT))
        py.display.set_caption('Game')

        wallpaper = py.image.load("wallpaper.jpg")
        menu = py.image.load("Backgroundunicorn.png")
        button = py.image.load("bouton-start.png")
        gameover = py.image.load("gameover.png")
        
        self.wallpaper = py.transform.scale(wallpaper, (WIDTH, HEIGHT))
        self.menu = py.transform.scale(menu, (WIDTH, HEIGHT))
        self.gameover = py.transform.scale(gameover, (WIDTH, HEIGHT))
        self.button = py.transform.scale(button, (170, 110))
        self.button_rect = self.button.get_rect()
        self.button_rect.x = 400
        self.button_rect.y = 300
        self.screen_scroll = 0

        # instance of Character and Enemy
        self.group_player = py.sprite.Group()
        self.player = Character(self)
        self.group_player.add(self.player) # add player to a goup to compare it with group_enemy
        self.group_enemy = py.sprite.Group()

        self.game_is_running = False
    
    # check if a sprite collide with a group of sprite
    def check_collision(self, sprite, group): 
        return py.sprite.spritecollide(sprite, group, False, py.sprite.collide_mask)# False to not kill the sprite
    
    # create enemy
    def spawn_enemy(self):
        self.group_enemy.add(Enemy(self))
    
    # display background
    def draw_bg(self):
        for i in range(5):
            # add successively a background after another one
            self.screen.blit(self.wallpaper,((i * WIDTH) + self.screen_scroll, bg_y)) 
    
    # move elements of the game according to the direction and the scroll
    def scroll(self, direction):
        # update enemy, screen_scroll and player coord according to player's velocity
        self.player.rect.x = self.player.rect.x - (-1)**direction * self.player.velocity
        for enemy in self.group_enemy :
            enemy.rect.x = enemy.rect.x - (-1)**direction * self.player.velocity
            for tank_proj in enemy.group_projectil :
                # update eney's projectil coord according to the direction of the scroll
                tank_proj.rect.x = tank_proj.rect.x - (-1)**direction * tank_proj.velocity
        self.screen_scroll = self.screen_scroll - (-1)**direction * self.player.velocity

    def run(self):
        # Main loop of the game
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    exit()

                if event.type == py.MOUSEBUTTONDOWN :
                    if self.button_rect.collidepoint(event.pos):
                        # launch the game
                        self.start()
            # ------------------------------------------------------------------------
            if self.game_is_running :
                self.play()
            else : 
                self.screen.blit(self.menu, (bg_x,bg_y))
                self.screen.blit(self.button,(self.button_rect.x, self.button_rect.y))
                                               
            
            """if event.type == py.KEYDOWN:
                # set the state at start at the begining
                self.gameStateManager.set_state()
            """
        
            """
            # launch the function run of level or start accroding to currentState
            self.states[self.gameStateManager.get_state()].run()
            if self.gameStateManager.get_state()== 'menu' :
                self.play()
            #print(self.gameStateManager.get_state())"""
            
            py.display.update()
            self.clock.tick(FPS)

    
    def start(self):
        self.game_is_running = True
        self.spawn_enemy()

    def end(self):
        self.group_enemy = py.sprite.Group()
        self.player.current_health = self.player.maximum_health
        #self.screen.blit(self.gameover, (bg_x,bg_y))
        self.game_is_running = False
    
    def level(self):
        text_font = py.font.SysFont("Arial", 30)
        score = text_font.render(str(self.player.score), True, COLOR['white'])
        self.screen.blit(score,(10, 10))

    def play(self):
        # DISPLAY
        self.draw_bg()
        self.screen.blit(self.player.image, self.player.rect) #display

        self.player.update_health_bar(self.screen)
        self.player.update() #Pour mettre à jour chaque frame la barre de vie afin de pouvoir la changer 
        self.level()
        if self.player.current_health <=0 :
            self.end()

        # Move projectils and enemies that are in groups
        for enemy in self.group_enemy:
            enemy.move()
            enemy.update_health_bar(self.screen)
            enemy.group_projectil.draw(self.screen)
            for projectile_tank in enemy.group_projectil:
                projectile_tank.move()
                

        for projectile_player in self.player.group_projectil:
            projectile_player.move()

        # display all enmies and projectiles groups
        self.group_enemy.draw(self.screen)
        self.player.group_projectil.draw(self.screen)
        """
        # à modifeier avec LOOSE
            elif event.type==screamer:
            # Marquer le début de l'affichage de l'image
            image_display_start = current_time
        if image_display_start:
            if current_time - image_display_start <= 1000:  # 100 ms = 1/10 de seconde
                game.screen.blit(special_image, (900, 900))  
            else:
                image_display_start = None  # Réinitialiser pour le prochain affichage
        """
        # song.play()        
            
        # KEYBOARD      
        keys_pressed = py.key.get_pressed()      
        if keys_pressed[py.K_LEFT] and self.player.rect.x >10:
            self.player.move_left()
            if self.player.rect.x <= x_init and self.screen_scroll<0:
                direction = 1
                self.scroll(direction)# move the screen 

        if keys_pressed[py.K_RIGHT] and self.player.rect.x<50000 :
            # collision check 
            self.player.move_rigth()
            if self.player.rect.x >= WIDTH - SCROLL_LIM :
                direction = 0
                self.scroll(direction)# move the screen

        if abs(self.screen_scroll) > WIDTH : 
            self.screen_scroll = 0 # reset screen_scroll if it's biggier than the width of the screen

        # launch player projectil if key space pressed
        if keys_pressed[py.K_SPACE]:
            self.player.launch_projectil()
            
        # player jumps if key up is pressed 
        if keys_pressed[py.K_UP]:
            self.player.jump_state = True
        if self.player.jump_state :
            self.player.jump()
        
        for enemy in self.group_enemy :
            # launch enemy's projectils randomly
            if random.randint(0,40)%20 == 0 and enemy.current_health >0 and enemy.rect.x < WIDTH and self.player.current_health >0:
                enemy.throw_projectile()

