import pygame as py
import random
from sys import *
from math import *

from var import *
from Enemy import *
from Character import *
from Mushspawn import *
from Platform import *

class Game :
    def __init__(self):
        py.init()
        random.seed()
        self.clock = py.time.Clock()
        #current_time = py.time.get_ticks()

        # Window
        self.screen = py.display.set_mode((WIDTH,HEIGHT))
        py.display.set_caption('Game')

        # Images
        self.current_level = 0
        wallpaper = py.image.load(WALLPAPER[self.current_level])
        print(WALLPAPER[self.current_level], self.current_level)
        menu = py.image.load("images/Backgroundunicorn.png")
        button = py.image.load("images/bouton-start.png")
        gameover = py.image.load("images/gameover.png")
        
        self.wallpaper = py.transform.scale(wallpaper, (WIDTH, HEIGHT))
        self.menu = py.transform.scale(menu, (WIDTH, HEIGHT))
        self.gameover = py.transform.scale(gameover, (400, 200))
        self.button = py.transform.scale(button, (170, 110))
        self.button_rect = self.button.get_rect()
        self.button_rect.x = 400
        self.button_rect.y = 300

        # Sound
        self.song = py.mixer.Sound("tqt.mp3")
        self.explosion_sound = py.mixer.Sound("Explosion sound.mp3")

        # instance of Character and Enemy
        self.group_player = py.sprite.Group()
        self.player = Character(self)
        self.group_player.add(self.player) # add player to a goup to compare it with group_enemy
        self.group_enemy = py.sprite.Group()
        self.mushspawn = Mushspawn()
        self.Groupe_Mush = py.sprite.Group()

	    # Instance for the platforms
        # Create a group to hold the platforms
        self.platform_coord_y = 280
        self.group_platforms = py.sprite.Group()
        platform1 = Platform(100, self.platform_coord_y, 200, 100)
        platform2 = Platform(600, self.platform_coord_y, 200, 100)
        self.group_platforms.add(platform1, platform2)
        self.game_is_running = False
        self.screen_scroll = 0
        self.direction = 0
    
    # check if a sprite collide with a group of sprite
    def check_collision(self, sprite, group): 
        return py.sprite.spritecollide(sprite, group, False, py.sprite.collide_mask)# False to not kill the sprite
    
    # create enemy
    def spawn_enemy(self):
        self.group_enemy.add(Enemy(self))
    
    def spawn_Mush(self):
        self.Groupe_Mush.add(Mushspawn())
    
    # display background
    def draw_bg(self):
        for i in range(5):
            # add successively a background after another one
            self.screen.blit(self.wallpaper,((i * WIDTH) + self.screen_scroll, bg_y)) 
    
    
    # move elements of the game according to the direction and the scroll
    def scroll(self):
        # update enemy, screen_scroll and player coord according to player's velocity
        self.player.rect.x = self.player.rect.x - (-1)**self.direction * self.player.velocity
        for enemy in self.group_enemy :
            enemy.rect.x = enemy.rect.x - (-1)**self.direction * self.player.velocity
            for tank_proj in enemy.group_projectil :
                # update eney's projectil coord according to the direction of the scroll
                tank_proj.rect.x = tank_proj.rect.x - (-1)**self.direction * tank_proj.velocity
        self.screen_scroll = self.screen_scroll - (-1)**self.direction * self.player.velocity

    def run(self):
        # Main loop of the game
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    exit()

                if event.type == py.MOUSEBUTTONDOWN :
                    if self.button_rect.collidepoint(event.pos):
                        self.start() # launch the game

            if self.game_is_running :
                self.play_game()
            else : 
                self.start_menu()
                                               
            
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

    def start_menu(self):
        self.screen.blit(self.menu, (bg_x,bg_y))
        self.screen.blit(self.button,(self.button_rect.x, self.button_rect.y))

    def start(self):
        self.game_is_running = True
        self.spawn_enemy()
        self.spawn_Mush()

    # rest all settings
    def end(self):
        #self.screen.blit(self.gameover, (320,100))
        #self.clock.tick(0.9)
        self.group_enemy = py.sprite.Group()
        self.game_is_running = False 
        self.current_level = 0
        # reset the first wallpaper
        self.wallpaper = py.transform.scale(py.image.load(WALLPAPER[self.current_level]), (WIDTH, HEIGHT))
        # rest player values
        self.player.current_health = self.player.maximum_health
        self.player.rect.x = x_init
        self.player.rect.y = y_init
        self.player.score = 0
        

    def level(self):
        # display score
        text_font = py.font.SysFont("Arial", 20)
        self.screen.blit(text_font.render('Score ', True, COLOR['black']),(10, 10))
        score = text_font.render(str(self.player.score), True, COLOR['black'])
        self.screen.blit(score,(60, 10))
       
        if self.player.score>= 1000 and self.current_level == 0:
            self.current_level +=1
            # change the background
            self.wallpaper = py.transform.scale(py.image.load(WALLPAPER[self.current_level]), (WIDTH, HEIGHT))
            # change enemy and its settings
            self.group_enemy = py.sprite.Group()      
            self.spawn_enemy()
            for enemy in self.group_enemy :
                enemy.velocity += 1
                enemy.attack += 10
            #creer des dico d'ennemy, de vitesse et de dégats lié et changer en fct du score
            # niveau final ?

    def play_game(self):
        # DISPLAY
        self.draw_bg()
        self.screen.blit(self.player.image, self.player.rect) #display


        #self.screen.blit(self.mushspawn.image, self.mushspawn.rect) #display
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

        # display all enmies and player's projectils
        self.group_enemy.draw(self.screen)
        self.player.group_projectil.draw(self.screen)
        
    ###########################################################################
            # Move projectils and enemies that are in groups
        for Mushspawn in self.Groupe_Mush:
            #Mushspawn.move()
            Mushspawn.Groupe_Mush.draw(self.screen)
            for Mush_project in Mushspawn.Groupe_Mush:
                Mush_project.move()

        # display all enmies and player's projectils
        self.Groupe_Mush.draw(self.screen)
        
    ###########################################################################    
    
        # draw the platforms
        self.group_platforms.draw(self.screen)
    

        for platform in self.group_platforms:
            if self.check_collision(self.player, self.group_platforms):
                # is the player higher than the platform ?
                if self.player.rect.y > platform.rect.bottom -10:
                # position at the top of the platform
                    self.player.rect.y = platform.rect.bottom -10
                    #self.player.jump_vel = 22
                # is the player still on the platform
                elif self.player.rect.y <= self.platform_coord_y:
                    self.player.jump_vel = 0

        """conflit entre les conditions : si le pero est sur la platefrom il ne peut pas sauter
        pq la position du joueur est ramenée à celle de la plateform
        -->mettre cette partie dans jump !"""
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
        #self.song.play()        POUR REMETTRE LA MUSIQUE C EST ICI
            
        # KEYBOARD      
        keys_pressed = py.key.get_pressed()      
        if keys_pressed[py.K_LEFT] and self.player.rect.x >10:
            self.player.move_left()
            if self.player.rect.x <= x_init and self.screen_scroll<0:
                self.direction = 1
                self.scroll()# move the screen 

        if keys_pressed[py.K_RIGHT] and self.player.rect.x<50000 :
            # collision check 
            self.player.move_rigth()
            if self.player.rect.x >= WIDTH - SCROLL_LIM :
                self.direction = 0
                self.scroll()# move the screen

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
                
        for Mushspawn in self.Groupe_Mush:
            # launch Mushroom randomly
            if random.randint(0,197)%99 == 0 : #taux de spawn choisi à l'arrache
               
                Mushspawn.move()
                Mushspawn.throw_projectile()

                