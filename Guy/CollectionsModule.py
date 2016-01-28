from enum import Enum

class TileType(Enum):
    OUTER_WALL = 1
    ROAD = 2
    BUILDABLE_SURFACE = 3
    PLAYER_BASE = 4



class Color(object):
    black = (0,0,0)
    white = (255, 255, 255)
    
    red = (200,0,0)
    green = (0,200,0)

    bright_red = (255,0,0)
    bright_green = (0,255,0)