# VARIABLES

COLOR={'green':(159,226,191), 
       "yellow":(255,233,122), 
       "orange": (244,164,96), 
       "red":(222,49,99),
       "black":(0,0,0),
       "white":(255,255,255),
       "blue_transparent":(204,239,255,180),
       "blue":(0,108,108),
       "dark_blue":(37,60,60)}

# list of dico keys
color_name = [*COLOR.keys()]
length_dico = 5

WALLPAPER = {0 :'images/wallpaper.png',
            1 :'images/wallpaper2.jpg'}

def change_color(x):
    if x>=650 :
       return COLOR['green']
    elif 350<=x<650 :
        return COLOR['yellow']
    elif 250<=x<350 :
        return COLOR['orange']
    return COLOR['red']

PLAYER = {}
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
x_init, y_init = 100,450            
# trajector var
g = 11  
v_init = 80

cloud="images/cloud.jpg"