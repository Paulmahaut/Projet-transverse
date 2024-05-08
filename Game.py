import pygame as py
import random
from sys import *
from math import *

from var import *
from Enemy import *
from Character import *
from trajectory import *


class Game :
    def __init__(self):
        py.init()
        random.seed()
        self.clock = py.time.Clock()
        #current_time = py.time.get_ticks()

        # Window
        self.screen = py.display.set_mode((WIDTH,HEIGHT))
        py.display.set_caption('Game')
        
        self.current_level = 0
        self.game_is_running = False
        self.screen_scroll = 0
        self.direction = 0
        self.clicked = False

        # Images
        wallpaper = py.image.load(WALLPAPER[self.current_level])
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
        self.song = py.mixer.Sound("sound/tqt.mp3")
        self.explosion_sound = py.mixer.Sound("sound/explosion_sound.mp3")

        # instance of Character and Enemy
        self.group_player = py.sprite.Group()
        self.player = Character(self)
        self.group_player.add(self.player) # add player to a goup to compare it with group_enemy
        self.group_enemy = py.sprite.Group()

        # trajectory
        self.clicked = False
        self.currentp = None
        self.pos = None
        self.theta = -30
        self.origin = (self.player.rect.x+46, self.player.rect.y+5) # at the top of the licorne
        
        self.arct = to_radian(self.theta)       
        self.end = pos_on_circumeference( self.theta,  self.origin)
        self.arcrect = py.Rect(self.origin[0]-30, self.origin[1]-30, 60, 60)

        self.font = py.font.SysFont('verdana', 12)

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
                py.event.clear
                self.play_game(event)
            else : 
                self.start_menu()

            py.display.update()
            self.clock.tick(FPS)

    def start_menu(self):
        self.screen.blit(self.menu, (bg_x,bg_y))
        self.screen.blit(self.button,(self.button_rect.x, self.button_rect.y))

    def start(self):
        self.game_is_running = True
        self.spawn_enemy()

    # rest all settings
    def end_game(self):
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
            #creer des dico d'ennemy, de vitesse et de dégats liés et changer en fct du score
            # niveau final ?

    def play_game(self, event):

        # DISPLAY
        self.draw_bg()
        self.screen.blit(self.player.image, self.player.rect) #display

        self.player.update_health_bar(self.screen)
        self.player.update() #Pour mettre à jour chaque frame la barre de vie afin de pouvoir la changer 
        self.level()
        if self.player.current_health <=0 :
            self.end_game()

        # Move projectils and enemies that are in groups
        for enemy in self.group_enemy:
            enemy.move()
            enemy.update_health_bar(self.screen)
            enemy.group_projectil.draw(self.screen)
            for projectile_tank in enemy.group_projectil:
                projectile_tank.move()

        # display all enmies and player's projectils
        self.group_enemy.draw(self.screen)
        #self.player.group_projectil.draw(self.screen)
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
        #self.song.play()        
            
        # KEYBOARD  

        # move to the left
        keys_pressed = py.key.get_pressed()      
        if keys_pressed[py.K_LEFT] and self.player.rect.x >10:
            self.player.move_left()
            if self.player.rect.x <= x_init and self.screen_scroll<0:
                self.direction = 1
                self.scroll()# move the screen 

        # move to the right
        if keys_pressed[py.K_RIGHT] and self.player.rect.x<50000 :
            # collision check 
            self.player.move_rigth()
            if self.player.rect.x >= WIDTH - SCROLL_LIM :
                self.direction = 0
                self.scroll()# move the screen
        
        # reset screen_scroll if it's biggier than the screen width  
        if abs(self.screen_scroll) > WIDTH : 
            self.screen_scroll = 0 
        
        # Projectil traj
        if event.type == py.MOUSEBUTTONDOWN:
            print(self.pos, self.end)
            if not self.clicked :
                self.clicked = True
        if event.type == py.MOUSEBUTTONUP:
            if self.clicked :
                self.clicked = False
                self.pos = event.pos # take the mouse position (x,y)
                if -90 < self.theta <= 0:
                    self.player.launch_projectil(self.theta, self.origin)
                    self.end = pos_on_circumeference(self.theta, self.origin)
                    self.arcrect = py.Rect(self.origin[0]-30, self.origin[1]-30, 60, 60)

        if event.type == py.MOUSEMOTION:
            if self.clicked:
                self.pos = event.pos # take the mouse position (x,y)
                self.theta = get_angle(self.pos, self.origin)
                if -90 < self.theta <= 0:
                    self.end = pos_on_circumeference(self.theta, self.origin)
                    self.arct = to_radian(self.theta)
    
                py.draw.line(self.screen, COLOR['red'], self.origin, (self.origin[0] + WIDTH-200, self.origin[1]), 2)
                py.draw.line(self.screen, COLOR['yellow'], self.origin, (self.origin[0], self.origin[1] - 250), 2)
                py.draw.line(self.screen, COLOR['black'], self.origin, self.end, 2)
                py.draw.circle(self.screen, COLOR['yellow'], self.origin, 3)
                py.draw.arc(self.screen, COLOR['orange'], self.arcrect, 0, -(self.arct), 2)

        self.player.group_projectil.update()
        # update origin
        self.origin = (self.player.rect.x+46, self.player.rect.y+5)
        # update the end of the guideline
        self.end = pos_on_circumeference(self.theta, self.origin)

        # Info *******************************************************************
        title = self.font.render("Projectile Motion", True, COLOR['white'])
        fpstext = self.font.render(f"FPS : {int(self.clock.get_fps())}", True, COLOR['white'])
        thetatext = self.font.render(f"Angle : {int(abs(self.theta))}", True, COLOR['white'])
        degreetext = self.font.render(f"{int(abs(self.theta))}°", True, COLOR['white'])
        self.screen.blit(title, (80, 30))
        self.screen.blit(fpstext, (20, 400))
        self.screen.blit(thetatext, (20, 420))
        self.screen.blit(degreetext, (self.origin[0]+38, self.origin[1]-20))

        py.draw.rect(self.screen, (0,0,0), (0, 0, WIDTH, HEIGHT), 5)
            
        # player jumps if key up is pressed 
        if keys_pressed[py.K_UP]:
            self.player.jump_state = True
        if self.player.jump_state :
            self.player.jump()
        
        for enemy in self.group_enemy :
            # launch enemy's projectils randomly
            if random.randint(0,40)%20 == 0 and enemy.current_health >0 and enemy.rect.x < WIDTH and self.player.current_health >0:
                enemy.throw_projectile()
        
        self.can_shoot = True

