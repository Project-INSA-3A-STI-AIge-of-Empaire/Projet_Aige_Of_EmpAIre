import math
import random

INITIAL_ZOOM = 1
MAX_ZOOM = 4
TILE_SIZE_2ISO = 15
TILE_SIZE_2D = 40
ONE_SEC = 1000 # 1000 millisec
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
MAP_CELLX = 120
MAP_CELLY = 120

UNIT_IDLE = 0
UNIT_WALKING = 1
UNIT_ATTACKING = 2
UNIT_DYING = 3

TREE_CAPACITY = 100
GOLD_CAPACITY = 800
FARM_CAPACITY = 300

#Menu constants

MODE_MENU = 0
MODE_TERMINAL = 1
MODE_ISO_2D = 2
MODE_PAUSE = 3


#MAP constants

NORMAL_MAP = 0
CENTERED_MAP = 1


from pvector2 import *
from ImageProcessingDisplay.imagemethods import * 
from ImageProcessingDisplay.viewport import ViewPort
from ImageProcessingDisplay.camera import Camera

UNIT_ANGLE_MAPPING = {
    0*math.pi/8:6,
    1*math.pi/8:5,
    2*math.pi/8:4,
    3*math.pi/8:3,
    4*math.pi/8:2,
    5*math.pi/8:1,
    6*math.pi/8:0,
    7*math.pi/8:15,
    8*math.pi/8:14,
    9*math.pi/8:13,
    10*math.pi/8:12,
    11*math.pi/8:11,
    12*math.pi/8:10,
    13*math.pi/8:9,
    14*math.pi/8:8,
    15*math.pi/8:7
}

PROJECTILE_ANGLE_MAPPING ={
    0*math.pi/8:6,
    1*math.pi/8:5,
    2*math.pi/8:4,
    3*math.pi/8:3,
    4*math.pi/8:2,
    5*math.pi/8:1,
    6*math.pi/8:0,
    7*math.pi/8:15,
    8*math.pi/8:14,
    9*math.pi/8:13,
    10*math.pi/8:12,
    11*math.pi/8:11,
    12*math.pi/8:10,
    13*math.pi/8:9,
    14*math.pi/8:8,
    15*math.pi/8:7
}

def MAP_ANGLE_INDEX(angle, angle_map):
    animation_index =0
    shortest_distance = 10 # big enoug so difference between two angle will never be that big

    for angle_key in angle_map.keys():
        current_distance = abs(angle - angle_key)
        if current_distance <= shortest_distance:
            shortest_distance = current_distance
            animation_index = angle_map.get(angle_key)

    return animation_index
 

camera = Camera()
font = pygame.font.Font(None, 24)


GRASS_ARRAY_1D = zoomlevels_sprite("Sprites/grass.webp", camera)

ARCHERYRANGE_1D = zoomlevels_sprite("Sprites/Building/archery_range.webp", camera)
BARRACKS_ARRAY_1D = zoomlevels_sprite("Sprites/Building/barracks.webp", camera)
CAMP_ARRAY_1D = zoomlevels_sprite("Sprites/Building/camp.webp", camera)
KEEP_ARRAY_1D = zoomlevels_sprite("Sprites/Building/keep.webp", camera)
TOWNCENTER_ARRAY_1D = zoomlevels_sprite("Sprites/Building/town_center_1.webp", camera)
FARM_ARRAY_1D = zoomlevels_sprite("Sprites/Building/farm.webp", camera)
GOLD_ARRAY_2D = zoomlevels_load_single_sprites("Sprites/Resources/gold.webp",7, camera)
TREES_ARRAY_2D = zoomlevels_load_single_sprites("Sprites/Resources/trees.webp",42, camera)
STABLE_ARRAY_2D = zoomlevels_load_single_sprites("Sprites/Building/stable.webp", 27, camera)
HOUSES_ARRAY_2D = zoomlevels_load_single_sprites("Sprites/Building/houses.webp",3, camera)
HORSEMAN_ARRAY_4D = state_zoomlevels_load_sprite_sheet("Sprites/Unit/horseman", camera)
ARCHER_ARRAY_4D =  state_zoomlevels_load_sprite_sheet("Sprites/Unit/archer", camera)
SWORDMAN_ARRAY_4D =state_zoomlevels_load_sprite_sheet("Sprites/Unit/swordman", camera)
VILLAGER_ARRAY_4D =state_zoomlevels_load_sprite_sheet("Sprites/Unit/villager", camera)

ARROW_ARRAY_3D = zoomlevels_load_sprite_sheet("Sprites/Projectile/arrow.webp",32, 11, camera, skip_row = 2, limit_col = 1)



CURSOR_IMG = pygame.image.load("Sprites/cursor.png")

