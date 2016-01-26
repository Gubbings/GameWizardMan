import CollectionsModule
import MenuModule
#import MapTileModule
import pygame
import Editor

#global variables
clock = pygame.time.Clock()
screenWidth = 800
screenHeight = 700
screenSize = screenWidth, screenHeight
mainSurface = pygame.display.set_mode(screenSize, pygame.RESIZABLE)


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

    #check if the mouse is hovering over the button
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
#    tile = Editor.MapTileModule.MapTile(0,0, CollectionsModule.TileType.ROAD) 

   
    #menu logo image
    logo = pygame.image.load("GameLogo.gif")
    logoRect = logo.get_rect()
    logoPos = (screenWidth / 2) - (logoRect.size[0]/2), (screenHeight / 4) - (logoRect.size[1]/2)


    
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit()

        #add the logo to the window
        mainSurface.blit(logo, logoPos)
     

        #placeholder rectangles that will be used for button
        button("Play", screenWidth / 2 - 50, 350, 100, 50, CollectionsModule.Color.white, CollectionsModule.Color.red, mainGameLoop)
        button("Tutorial", screenWidth / 2 - 50, 425, 100, 50, CollectionsModule.Color.white, CollectionsModule.Color.red)
        button("Settings", screenWidth / 2 - 50, 500, 100, 50, CollectionsModule.Color.white, CollectionsModule.Color.red)
        button("Quit", screenWidth / 2 - 50, 575, 100, 50, CollectionsModule.Color.white, CollectionsModule.Color.red, exit)

        pygame.display.flip()
        #60fps or lower
        clock.tick(60)


    tileSize = 100, 100

    diamond = pygame.image.load("diamond.jpg")
    pygame.transform.scale(diamond, tileSize)
    diamondRect = diamond.get_rect()





#----------------------------------------------------------------------
#   MAIN GAME LOOP
#----------------------------------------------------------------------
def mainGameLoop():
    mainSurface.fill(CollectionsModule.Color.black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit()

        
        for i in range(0, 5):
            for j in range(0, 5):
                tile = pygame.draw.rect(mainSurface, (255,0,0), (100 * i, j * 100,100,100), 1)
                
            
        Editor.getTileSheet(mainSurface, "Assets/TileSets/tileset1.png", 24, 16, True, 550, 50)

        pygame.display.update()

        clock.tick(60)
        #update the display
        #pygame.display.flip()


#exit pygame and quit the program
def exit():
    pygame.quit()
    quit()


#entry point for the entire game
mainInit()

