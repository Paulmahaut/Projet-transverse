# VARIABLES

COLOR={'green':(159,226,191), 
       "yellow":(255,233,122), 
       "orange": (244,164,96), 
       "red":(222,49,99),
       "black":(0,0,0)}

WALLPAPER = {0 :'images/wallpaper1.jpg',
            1 :'images/wallpaper2.jpg'}

def change_color(x):
    if x>=650 :
       return COLOR['green']
    elif 350<=x<650 :
        return COLOR['yellow']
    elif 250<=x<350 :
        return COLOR['orange']
    return COLOR['red']

ENEMY = {0 : "images/tank0.png",
         1: "images/tank1.png"
         }

ENEMY_PROJ = {0: "images/tank_proj0.png",
              1: "images/tank_proj1.png"
              }

PLAYER = {0 : "images/licorne_right.png",
          1 : "images/licorne_left.png"}
PLAYER_PROJ = {}

LOOSE = False
TANK_SHOOT = 0
FPS = 60
WIDTH = 1000
HEIGHT = 700
SCROLL_LIM = 500

#coord of background
bg_x, bg_y=0,0
#initial coord of player
x_init, y_init = 100,430

