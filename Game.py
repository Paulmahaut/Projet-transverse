import pygame as py
import random
from sys import *
from math import *

from var import *
from Enemy import *
from Character import *
from trajectory import *
from Mushspawn import *
from Small_Enemy import *


class Game :
    def __init__(self):
        py.init()
        random.seed()
        self.clock = py.time.Clock()
        #current_time = py.time.get_ticks()

        # Window
        self.screen = py.display.set_mode((WIDTH,HEIGHT))
        py.display.set_caption('UNICORN VS TANKS')

        self.game_is_running = False
        self.screen_scroll = 0
        self.direction = 0
        self.all_scores = []

        # Images
        wallpaper = py.image.load("images/wallpaper.png")
        menu = py.image.load("images/Backgroundunicorn.png")
        self.wallpaper = py.transform.scale(wallpaper, (WIDTH, HEIGHT))
        self.menu = py.transform.scale(menu, (WIDTH, HEIGHT))

        # layout
        self.font = py.font.SysFont('verdana', 12)
        self.surface1 = py.Surface((WIDTH,HEIGHT), py.SRCALPHA)
        self.surface2 = py.Surface((WIDTH,HEIGHT), py.SRCALPHA)
        self.font_start_title = py.font.SysFont('verdana', 23, bold = True)
        self.font_start = py.font.SysFont('verdana', 19)
        self.font_start2 = py.font.SysFont('verdana', 19, True)

        # Sound
        self.song = py.mixer.Sound("sound/tqt.mp3")
        self.explosion_sound = py.mixer.Sound("sound/explosion_sound.mp3")

        # Instances 
        self.group_player = py.sprite.Group()
        self.player = Character(self)
        self.group_player.add(self.player) # add player to a goup to compare it with groups
        self.group_enemy = py.sprite.Group()
        self.group_small_enemy = py.sprite.Group()
        self.mushspawn = Mushspawn(self)
        self.group_cloud = py.sprite.Group()

        # trajectory
        self.clicked = False
        self.currentp = None
        self.pos = None
        self.theta = -30
        self.origin = (self.player.rect.x+128, self.player.rect.y+5) # at the top of the licorne
        
        self.arct = to_radian(self.theta)       
        self.end = pos_on_circumeference( self.theta,  self.origin, self.player.sign)
        self.arcrect = py.Rect(self.origin[0]-30, self.origin[1]-30, 60, 60)


    # check if a sprite collide with a group of sprite
    def check_collision(self, sprite, group): 
        return py.sprite.spritecollide(sprite, group, False, py.sprite.collide_mask)# False to not kill the sprite
    
    # create enemy
    def spawn_enemy(self):
        self.group_enemy.add(Enemy(self))
    
    # create small enemy
    def spawn_small_enemy(self):
        self.group_small_enemy.add(Small_Enemy(self))
    
    def spawn_cloud(self):
        self.group_cloud.add(Mushspawn(self))
    
    # display background
    def draw_bg(self):
        for i in range(5):
            # add successively a background after another one
            self.screen.blit(self.wallpaper,((i * WIDTH) + self.screen_scroll, bg_y)) 
    
    # move elements of the game according to the direction and the scroll
    def scroll(self):
        # update elements coord according to player's velocity
        self.player.rect.x = self.player.rect.x - (-1)**self.direction * self.player.velocity
        # cloud
        for cloud in self.group_cloud:
            cloud.rect.x = cloud.rect.x - (-1)**self.direction * self.player.velocity
            for mushroom in cloud.group_mush:
                mushroom.rect.x =  mushroom.rect.x - (-1)**self.direction * self.player.velocity
        # player projectil
        for projectil in self.player.group_projectil:
            projectil.rect.x = projectil.rect.x - (-1)**self.direction * self.player.velocity
        for enemy in self.group_enemy :
            enemy.rect.x = enemy.rect.x - (-1)**self.direction * self.player.velocity
            #enemy projectil
            for tank_proj in enemy.group_projectil :
                tank_proj.rect.x = tank_proj.rect.x - (-1)**self.direction * tank_proj.velocity
        for small_enemy in self.group_small_enemy :
            small_enemy.rect.x = small_enemy.rect.x - (-1)**self.direction * self.player.velocity
        self.screen_scroll = self.screen_scroll - (-1)**self.direction * self.player.velocity

    def run(self):
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    exit()

                if event.type == py.KEYDOWN:
                    # launch the game if a key shift is pressed
                    if (event.key == py.K_RSHIFT or event.key == py.K_LSHIFT) and self.game_is_running == False:
                        self.start()
    
            if self.game_is_running :
                py.event.clear
                self.play_game(event)
            else : 
                self.start_menu()

            py.display.update()
            self.clock.tick(FPS)

    def start_menu(self):
        # first menu without score
        if len(self.all_scores) == 0:
            self.screen.blit(self.menu, (bg_x,bg_y))
            self.screen.blit(self.surface1, (0,0))
            py.draw.rect(self.surface1, COLOR["blue_transparent"] , [150,100, 700,400], 0, 10)
            start_title = self.font_start_title.render("Welcome in a new adventure !", True, COLOR['blue'])
            self.screen.blit(start_title, (300, 150))

            info = ["Things to know before to play: ",
                    "  - Key Q or left arrow to move left", 
                    "  - Key D or right arrow to move right", 
                    "  - Key Z, space or up arrow to jump",
                    "  - use the touch pad to shoot"]
            y = 200
            for line in info:
                start_msg = self.font_start.render(line, True, COLOR['dark_blue'])
                self.screen.blit(start_msg, (320, y))
                y+=30
        
            msg = self.font_start2.render("You can press the shift key to start ", True,  COLOR['blue'])
            self.screen.blit(msg, (280, y+30))
            key = py.image.load("images/shift.png")
            key = py.transform.scale(key, (70, 70))
            self.screen.blit(key, (470, y+60))

        # second menu with score
        else:
            # left block with message
            self.screen.blit(self.menu, (bg_x,bg_y))
            self.screen.blit(self.surface2, (0,0))
            py.draw.rect(self.surface2, COLOR["blue_transparent"] , [100,100, 490,400], 0, 10)
            start_title = self.font_start_title.render("Welcome back !", True, COLOR['blue'])
            self.screen.blit(start_title, (190, 150))

            info = ["Reminder: ",
                    "  - Key Q or left arrow to move left", 
                    "  - Key D or right arrow to move right", 
                    "  - Key Z, space or up arrow to jump",
                    "  - use the touch pad to shoot"]
            y = 200
            for line in info:
                start_msg = self.font_start.render(line, True, COLOR['dark_blue'])
                self.screen.blit(start_msg, (140, y))
                y+=30
        
            msg = self.font_start2.render("Press the shift key to play again ", True,  COLOR['blue'])
            self.screen.blit(msg, (150, y+30))
            key = py.image.load("images/shift.png")
            key = py.transform.scale(key, (70, 70))
            self.screen.blit(key, (240, y+60))

            # right block with the score
            py.draw.rect(self.surface2, COLOR["blue_transparent"] , [600,100, 300,320], 0, 10)
            score_title = self.font_start_title.render("Your best scores", True, COLOR['blue'])
            self.screen.blit(score_title, (640, 150))
            self.all_scores.sort(reverse = True)
            if len(self.all_scores)<5:
                lim = len(self.all_scores)
            else:
                lim = 5
            y = 200
            for i in range(lim):
                score = self.font_start.render(f'{i+1}. '+ str(self.all_scores[i]), True, COLOR['dark_blue'])
                self.screen.blit(score, (670, y))
                y+=30


    def start(self):
        self.game_is_running = True
        self.spawn_enemy()
        self.spawn_small_enemy()
        self.spawn_cloud()
        self.player = Character(self)
        self.group_player.add(self.player)

    # rest all settings
    def end_game(self):
        # save the score
        self.all_scores.append(self.player.score)
        # kill elements in class
        for enemy in self.group_enemy:
            for proj in enemy.group_projectil:
                proj.kill()
            enemy.kill()
        for cloud in self.group_cloud:
            for mushroom in cloud.group_mush:
                mushroom.kill()
            cloud.kill()

        for player in self.group_player:
            for projectil in player.group_projectil:
                projectil.kill()
            player.kill()
        # rest groups
        self.group_cloud = py.sprite.Group()
        self.group_enemy = py.sprite.Group()
        self.group_small_enemy = py.sprite.Group()
        self.group_player = py.sprite.Group()

        self.game_is_running = False 
        # rest player values
        self.player.current_health = self.player.maximum_health
        self.player.rect.x = x_init
        self.player.rect.y = y_init
        self.player.score = 0
    
    def display_score(self):
        # display score
        text_font = py.font.SysFont("Arial", 20)
        self.screen.blit(text_font.render('Score ', True, COLOR['black']),(10, 10))
        score = text_font.render(str(self.player.score), True, COLOR['black'])
        self.screen.blit(score,(60, 10))
        
    def play_game(self, event):

        # DISPLAY
        self.draw_bg()

        # border of the screen
        py.draw.rect(self.screen, COLOR["white"], (0, 0, WIDTH, HEIGHT), 5)

        self.display_score()
        
        # display player
        self.screen.blit(py.transform.flip(self.player.image, self.player.flip, False), self.player.rect)

        self.player.update_health_bar(self.screen)
        self.player.update() # update health bar of the player

        self.song.play()  
        
        # game over
        if self.player.current_health <=0 :
            self.end_game()

        # Move projectils and enemies that are in groups
        for enemy in self.group_enemy:
            enemy.move()
            enemy.update_health_bar(self.screen)
            # draw projectil
            enemy.group_projectil.draw(self.screen)
            for projectile_tank in enemy.group_projectil:
                projectile_tank.move()
        
        # Move small_enemies that are in groups
        for small_enemy in self.group_small_enemy:
            small_enemy.move()

        # display all enmies
        self.group_enemy.draw(self.screen)
        self.group_small_enemy.draw(self.screen)

        # Move mushrooms and clouds that are in groups
        for cloud in self.group_cloud:
            cloud.move()
            # draw projectil
            cloud.group_mush.draw(self.screen)
            for cloud_proj in cloud.group_mush:
                cloud_proj.move()

        # display all clouds
        self.group_cloud.draw(self.screen)     
            
        # list of keys
        keys_pressed = py.key.get_pressed()

        # move to the left
        keys_pressed = py.key.get_pressed()      
        if (keys_pressed[py.K_q] or keys_pressed[py.K_LEFT]) and self.player.rect.x >10:
            self.player.move_left()
            if self.player.rect.x <= x_init and self.screen_scroll<0:
                self.direction = 1
                self.scroll()# move the screen 

        # move to the right
        if (keys_pressed[py.K_d] or keys_pressed[py.K_RIGHT]) and self.player.rect.x<50000 :
            # collision check 
            self.player.move_rigth()
            if self.player.rect.x >= WIDTH - SCROLL_LIM :
                self.direction = 0
                self.scroll()# move the screen

        # player jumps if key space is pressed 
        if keys_pressed[py.K_SPACE]or keys_pressed[py.K_z] or keys_pressed[py.K_UP]:
            self.player.jump_state = True
        if self.player.jump_state :
            self.player.jump()
        
        # reset screen_scroll if it's biggier than the screen width  
        if abs(self.screen_scroll) > WIDTH : 
            self.screen_scroll = 0 

        # https://github.com/pyGuru123/Simulations/blob/main/Projectile%20Motion/main.py        
        # Projectil ******************************************************************
        if event.type == py.MOUSEBUTTONDOWN:
            if not self.clicked :
                self.clicked = True
                self.arcrect = py.Rect(self.origin[0]-30, self.origin[1]-30, 60, 60)

        if event.type == py.MOUSEBUTTONUP:
            if self.clicked :
                self.clicked = False
                self.pos = event.pos # take the mouse position (x,y)
                # to shoot rihgt
                if -90 < self.theta <= 0 and not self.player.flip:
                    self.player.launch_projectil(self.theta, self.origin, self.player.sign)
                    self.end = pos_on_circumeference(self.theta, self.origin,self.player.sign)
                # to shoot left
                elif 0 < self.theta < 90 and self.player.flip: 
                    self.player.launch_projectil(self.theta, self.origin, self.player.sign)
                    self.end = pos_on_circumeference(self.theta, self.origin, self.player.sign)

        if event.type == py.MOUSEMOTION:
            if self.clicked:
                self.pos = event.pos # take the mouse position (x,y)
                self.theta = get_angle(self.pos, self.origin)
                # to shoot rihgt
                if -90 < self.theta <= 0 and not self.player.flip:
                    self.end = pos_on_circumeference(self.theta, self.origin, self.player.sign)
                    self.arct = to_radian(self.theta)

                    # display axis to shoot
                    py.draw.aaline(self.screen, COLOR['white'], self.origin, (self.origin[0] + 200, self.origin[1]), 2)
                    py.draw.aaline(self.screen, COLOR['white'], self.origin, (self.origin[0], self.origin[1] - 200), 2)
                    py.draw.line(self.screen, COLOR['white'], self.origin, self.end, 2)
                    py.draw.circle(self.screen, COLOR['yellow'], self.origin, 3)
                    py.draw.arc(self.screen, COLOR['orange'], self.arcrect, 0, -(self.arct), 2)
                
                # to shoot left
                elif 0 < self.theta <= 90 and self.player.flip:
                    self.end = pos_on_circumeference(self.theta, self.origin, self.player.sign)
                    self.arct = to_radian(self.theta)
                    print("arct :",self.arct, "theta :", self.theta)

                    # display axis to shoot
                    py.draw.aaline(self.screen, COLOR['white'], self.origin, (self.origin[0] - 200, self.origin[1]), 2)
                    py.draw.aaline(self.screen, COLOR['white'], self.origin, (self.origin[0], self.origin[1] - 200), 2)
                    py.draw.line(self.screen, COLOR['white'], self.end, self.origin, 2)
                    py.draw.circle(self.screen, COLOR['yellow'], self.origin, 3)
                    py.draw.arc(self.screen, COLOR['orange'], self.arcrect, -(pi + (self.arct)), -pi, 2)


        self.player.group_projectil.update()
        # update origin
        self.origin = (self.player.rect.x+128, self.player.rect.y+5)
        # update the end of the guideline to shoot
        self.end = pos_on_circumeference(self.theta, self.origin, self.player.sign)
        # update the rectangle of the arc
        self.arcrect = py.Rect(self.origin[0]-30, self.origin[1]-30, 60, 60)

        # Info *******************************************************************
        title = self.font.render("Info", True, COLOR['white'])
        fpstext = self.font.render(f"FPS : {int(self.clock.get_fps())}", True, COLOR['white'])
        thetatext = self.font.render(f"Angle : {int(abs(self.theta))}", True, COLOR['white'])
        self.screen.blit(title, (20, 40))
        self.screen.blit(fpstext, (20, 60))
        self.screen.blit(thetatext, (20, 80))

        # *************************************************************************
        
        # launch enemy's projectils randomly
        for enemy in self.group_enemy :
            if random.randint(0,100)%30 == 0 and enemy.current_health >0 and enemy.rect.x < WIDTH and self.player.current_health >0:
                enemy.throw_projectile()
        
        # launch Mushroom randomly
        for cloud in self.group_cloud:
            if random.randint(0,197)%99 == 0 : 
                cloud.throw_projectile()


