import pygame

def load_tile_table(filename, width, height):
    tileSheet = pygame.image.load(filename).convert()
    tileSheet_width, tileSheet_height = tileSheet.get_size()
    tile_table = []

    for tile_x in range(0, tileSheet_width / width):
        line = []
        tile_table.append(line)

        for tile_y in range(0, tileSheet_height / height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(tileSheet.subsurface(rect))

    return tile_table



#shows the tiles of a tilesheet split apart 
def getTileSheet(surface, tileSheetPath, tileWidth, tileHeight, render=False, xPos=0, yPos=0):
    tileTable = load_tile_table(tileSheetPath, tileWidth, tileHeight)

    for x, row in enumerate(tileTable):
        for y, tile in enumerate(row):
            if(render):
                surface.blit(tile, (x*32 + xPos, y*24 + yPos))

    return tileTable
