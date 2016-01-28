import CollectionsModule
import MenuModule
import MapTileModule
import pygame
import Editor

#global variables
clock = pygame.time.Clock()
screenWidth = 800
screenHeight = 700
screenSize = screenWidth, screenHeight
mainSurface = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
tileSheetTile = None
selectedTileSheet = None
selectedTileType = None
selectedTileTypeNum = None
mapTiles = [[None] * 5] * 5

#function used for primary initialization 
def mainInit():
    pygame.init()
   

    backgroundColor = 66, 61, 60
    mainSurface.fill(backgroundColor)

    initGame()

'''
    menuChoice = MenuModule.initMenu("diamond.gif")
    if(menuChoice == "Play"):
        initGame()
'''

#function used for rendering text - returns a surface and the associated rectangle for that surface
def text_objects(text, font):
    textSurface = font.render(text, True, CollectionsModule.Color.black)
    return textSurface, textSurface.get_rect()


#function that displays a pygame button
#   x,y = topleft corner position
#   msg = text in the button
def button(msg, x, y, width, height, normalColor, hoverColor, callbackFunction = None):

    #mouse position
    mouse = pygame.mouse.get_pos()

    #get state of the left mouse button
    leftMouseDown = pygame.mouse.get_pressed()[0] == 1

    #check if the mouse is over the button
    if ((x + width) > mouse[0] > x) and ((y + height) > mouse[1] > y):
        pygame.draw.rect(mainSurface, hoverColor, (x, y, width, height))

        if leftMouseDown and callbackFunction != None:
            callbackFunction()

    else:
        pygame.draw.rect(mainSurface, normalColor, (x, y, width, height))
    
        
    if msg != "":
        smallText = pygame.font.Font("Assets/Fonts/EdselFont.ttf", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (width / 2)), (y + (height / 2)))
        mainSurface.blit(textSurf, textRect)
        


        
#setup pygame window and main menu   
def initGame():
   
    #menu logo image
    logo = pygame.image.load("GameLogo.gif")
    logoRect = logo.get_rect()
    logoPos = (screenWidth / 2) - (logoRect.size[0]/2), (screenHeight / 4) - (logoRect.size[1]/2)


    #game loop using while the menu is active
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit()

        #add the logo to the window
        mainSurface.blit(logo, logoPos)
     

        #rectangles that will be used for buttons - some are placeholders
        button("Play", screenWidth / 2 - 50, 350, 100, 50, CollectionsModule.Color.white, CollectionsModule.Color.red, mainGameLoop)
        button("Tutorial", screenWidth / 2 - 50, 425, 100, 50, CollectionsModule.Color.white, CollectionsModule.Color.red)
        button("Settings", screenWidth / 2 - 50, 500, 100, 50, CollectionsModule.Color.white, CollectionsModule.Color.red)
        button("Quit", screenWidth / 2 - 50, 575, 100, 50, CollectionsModule.Color.white, CollectionsModule.Color.red, exit)
        
        #update entire display 
        pygame.display.flip()

        #60fps or lower
        clock.tick(60)






#----------------------------------------------------------------------
#   MAIN GAME LOOP
#----------------------------------------------------------------------
def mainGameLoop():
    
    #black background
    mainSurface.fill(CollectionsModule.Color.black)

    #game loop
    while True:
        global selectedTileSheet
        global mapTiles
        global selectedTileType
        mapTileSize = 100, 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                saveMap("Map1", mapTiles)
                exit()

        #mouse position
        mouse = pygame.mouse.get_pos()

        #get state of the left mouse button
        leftMouseDown = pygame.mouse.get_pressed()[0] == 1

        #show the tilesheet and get the 2D array representing all the tilesheet tiles
        tileTable = Editor.getTileSheet(mainSurface, "Assets/TileSets/tileset1.png", 24, 16, True, 550, 50)
        
        global tileSheetTile
        for i in range(0, len(tileTable)):
            for j in range(0, len(tileTable[0])):
#                if ((x + width) > mouse[0] > x) and ((y + height) > mouse[1] > y):
                if((i * 32 + 550 + 32) > mouse[0] > i * 32 + 550) and ((j * 24 + 50 + 32) > mouse[1] >  j * 24 + 50):
                    if(leftMouseDown):
                        tileSheetTile = tileTable[i][j]
                        selectedTileSheetTile = (i, j)
        

        global selectedTileTypeNum
        for i in range(1, 5):
             selectedTileTypeNum = i
             button(str(i), 550 + (i - 1) * 50, 200, 25, 25, CollectionsModule.Color.green, CollectionsModule.Color.red, setSelectedTileType) 
        

        #draw the red rectangles
        for i in range(0, 5):
            
            for j in range(0, 5):
                tile = pygame.draw.rect(mainSurface, (255,0,0), (i * mapTileSize[0], j * mapTileSize[1], mapTileSize[0], mapTileSize[0]), 3)
                    
                #if a map tile was selected from the tilesheet check if the user clicked a rectangle to paint it
                if tileSheetTile != None and selectedTileType != None:
                    if ((100 * i + 100) > mouse[0] > 100 * i) and ((100 * j + 100) > mouse[1] > 100 * j):
                        if(leftMouseDown):
                            tileSheetTile = pygame.transform.scale(tileSheetTile, mapTileSize)
                            mainSurface.blit(tileSheetTile, (i * mapTileSize[0], j * mapTileSize[1]))            
                            mapTiles[i][j] = MapTileModule.MapTile((i,j), selectedTileSheetTile, selectedTileType)

        pygame.display.update()
        clock.tick(60)


def setSelectedTileType():
    global selectedTileTypeNum
    global selectedTileType
    if(selectedTileTypeNum == 1):
        selectedTileType = CollectionsModule.TileType.OUTER_WALL
    if(selectedTileTypeNum == 2):
        selectedTileType = CollectionsModule.TileType.ROAD
    if(selectedTileTypeNum == 3):
        selectedTileType = CollectionsModule.TileType.BUILDABLE_SURFACE
    if(selectedTileTypeNum == 4):
        selectedTileType = CollectionsModule.TileType.PLAYER_BASE
    print(selectedTileType)        


def saveMap(fileName, mapTilesArray):
    if fileName != "":
#        f = open("Assets/Maps/".join(fileName).join("txt"), 'w')
        f = open("Assets/Maps/map1.txt", 'w')        
        
        for i in range(0, len(mapTilesArray)):
            for j in range(0, len(mapTilesArray[0])):
                if(mapTilesArray[i][j] != None):
                    f.write(str(mapTilesArray[i][j].mapPos) + ", " + str(mapTilesArray[i][j].tilesheetPos) + ", " + str(mapTilesArray[i][j].tileType) + "\n")

        print "Map Saved"
        f.close()

#exit pygame and quit the program
def exit():
    pygame.quit()
    quit()



#entry point for the entire game
mainInit()

