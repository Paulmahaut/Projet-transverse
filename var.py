# VARIABLES

COLOR={'green':(159,226,191), 
       "yellow":(255,233,122), 
       "orange": (244,164,96), 
       "red":(222,49,99)}

def change_color(x):
    if x>=650 :
       return COLOR['green']
    elif 350<=x<650 :
        return COLOR['yellow']
    elif 250<=x<350 :
        return COLOR['orange']
    return COLOR['red']


LOOSE = False
TANK_SHOOT = 0
FPS = 60
WIDTH = 1000
HEIGHT = 700
SCROLL_LIM = 500
#screen_scroll = 0
direction = 0

#coord of background
bg_x, bg_y=0,0
#initial coord of player
x_init, y_init = 100,430

