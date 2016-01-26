class MapTile(object):
    """description of class"""
    
    #index of the tile on the map - 0 based
    mapPos = 0,0

    #index of the image from the tilesheet
    tilesheetPos = 0,0

    #type of the square defined in the CollectionsModule file
    tileType = None

    #constructor
    def __init__(self, mapPos, tilesheetPos, tileType):
        self.mapPos = mapPos
        self.tilesheetPos = tilesheetPos
        self.tileType = tileType



