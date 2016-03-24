#Authors: Guy Coccimiglio, William Sigouin, Michael Thomas, Justin Rhude
#Game Software Engineering - Final Project - Tower Defense Game
#Prototype Version: 2.0
#Description: This python file controls initialization and all game logic
#   including rendering the game, controls and AI  

import pygame
from pytmx.util_pygame import load_pygame
import CollectionsModule
import Tower
import Bullet
import Enemy

#clock for controlling the FPS
clock = pygame.time.Clock()

#screen parameters
playableWidth = 700
screenWidth = 850
screenHeight = 575
screenSize = screenWidth, screenHeight
mainSurface = pygame.display.set_mode(screenSize)

#image for the tile selection sprite
tileSelectSprite = pygame.image.load("Assets/selectSprite.gif")

#tiled map
map1 = load_pygame("Assets/Maps/testMap.tmx")


#function used for primary initialization of pygame and background color
#this is used as the entry point into the game logic
def mainInit():
    #initialize pygame
    pygame.init()
    pygame.joystick.init()
          
    #set the background color
    backgroundColor = 66, 61, 60
    mainSurface.fill(backgroundColor)

    initGame()


#function used for rendering text - returns a surface and the associated rectangle for that surface
def text_objects(text, font):
    #render the text with a color of black
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
        #change button to have a different color when hovered over
        pygame.draw.rect(mainSurface, hoverColor, (x, y, width, height))

        if leftMouseDown and callbackFunction != None:
            callbackFunction()

    else:
        #change button back the normal color
        pygame.draw.rect(mainSurface, normalColor, (x, y, width, height))
    
   
    #if the button has text display it     
    if msg != "":
        smallText = pygame.font.Font("Assets/Fonts/EdselFont.ttf", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (width / 2)), (y + (height / 2)))
        mainSurface.blit(textSurf, textRect)
        


        
#setup pygame window and main menu   
def initGame():
    pygame.display.set_caption("Labyrinth Thief")

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
        
        #no longer needed - we might add the quit button back at a later time
        #button("Quit", screenWidth / 2 - 50, 575, 100, 50, CollectionsModule.Color.white, CollectionsModule.Color.red, exit)
        
        #update entire display 
        pygame.display.flip()

        #60fps or lower
        clock.tick(60)





#----------------------------------------------------------------------
#   MAIN GAME LOOP
#   Controls AI, rendering and joystick controls 
#----------------------------------------------------------------------
def mainGameLoop():    

    controller = None
    if(pygame.joystick.get_count() > 0):
        #get the first connected joystick     
        controller = pygame.joystick.Joystick(0)   
        controller.init()             

    #black background
    mainSurface.fill(CollectionsModule.Color.black)


    #get the object group with our AI path nodes
    path = map1.get_layer_by_name("EnemyPath")

    nodes = []
    # iterate through nodes in the object group:
    for node in path:
        nodes.append(node)

    #sort the list of path nodes
    nodes.sort()


    #get the object group with that marks the buildable surface area
    buildableArea = map1.get_layer_by_name("Buildable")
    buildableList = []
    for area in buildableArea:
        buildableList.append(area)


    #group of tower sprites
    towerList = pygame.sprite.Group()
    Tower.Tower.groups = towerList   

    #group of bullet sprites
    bulletList = pygame.sprite.Group()
    Bullet.Bullet.groups = bulletList
        
    #group of enemy sprites
    enemyList = pygame.sprite.Group()
    Enemy.Enemy.groups = enemyList
    Enemy.Enemy.towerGroup = towerList
    Enemy.Enemy.bulletGroup = bulletList


    #create an enemy
    enemyGif = pygame.transform.scale(pygame.image.load("Assets/Sprites/enemy1.png"), (32,32))    
    enemy = Enemy.Enemy(nodes, enemyGif)
    
    #create a tower
    towerGif = pygame.image.load("Assets/Sprites/towerTemp.gif")
    tower = Tower.Tower(towerGif, (32, 32), enemy)    
    
    #position of the tile selection sprite    
    selectSpriteX = 0
    selectSpriteY = 0
    #create a new user event for tracking joystick movement        
    JOYSTICK_MOVE_EVENT = pygame.USEREVENT+1

    #check if we have a controller before performing anything that pertains to the controller
    if(controller != None):            
        #get the bounds of the tiled map
        xBound = playableWidth
        yBound = screenHeight
        for x, y, image in map1.layers[0].tiles():                
            if(x > xBound):
                xBound = x
            if(y > yBound):
                yBound = y

        #time between JOYSTICK_MOVE_EVENTs
        timeBetweenEvents = 250

        #cause a joystick move event every 't' milliseconds where 't' is defined as timeBetweenEvents
        pygame.time.set_timer(JOYSTICK_MOVE_EVENT, timeBetweenEvents)

    #game loop
    while True:

        #check for pygame events                                      
        for event in pygame.event.get():                        
            if event.type == pygame.QUIT: 
                exit()

            #check if user clicked the 'A' button
            if event.type == pygame.JOYBUTTONDOWN:
                if controller.get_button(0):                    
                    #TODO: tower targets is currently hard coded we will base it on proximity in the future
                    #TODO: make towers cost resources
                    for area in buildableList:
                        #make sure the selection is horizontally and vertically in a buildable area
                        if(selectSpriteX * 32 > area.x and selectSpriteX * 32 < area.width):
                            if(selectSpriteY * 32 > area.y and selectSpriteY * 32 < area.height):
                                #spawn a new tower
                                Tower.Tower(towerGif, (selectSpriteX * 32, selectSpriteY * 32), enemy)

            #read joystick position for a joystick move event
            if event.type == JOYSTICK_MOVE_EVENT:                
                                               
                #position of the joystick axis
                h_axis = controller.get_axis(0)        
                v_axis = controller.get_axis(1)
                deadZone = 0.5

                #check if user is moving the joystick horizontally
                if(h_axis < -deadZone):            
                    if(selectSpriteX > 0):
                        selectSpriteX -= 1                                
                elif(h_axis > deadZone):
                    if(selectSpriteX < xBound):
                        selectSpriteX += 1
                
                #check if user is moving the joystick vertically
                if(v_axis < -deadZone):
                    if(selectSpriteY > 0):
                        selectSpriteY -= 1                
                elif(v_axis > deadZone):
                    if(selectSpriteY < yBound):
                        selectSpriteY += 1

        #display all of the tiles from the tiled map
        for layer in map1.layers:
            #we have marked object layers as invisible because they have no images 
            #only get the layers that are visible
            if layer.visible:
                for x, y, image in layer.tiles():                
                    mainSurface.blit(image, (32 * x, 32 * y))                  

        #update tower sprites
        towerList.update()
        towerList.draw(mainSurface)        
        
        #update bullet sprites
        bulletList.update()
        bulletList.draw(mainSurface)
        
        #update the enemy sprites
        enemyList.update()
        enemyList.draw(mainSurface)
        

        #display the tile selection sprite
        mainSurface.blit(tileSelectSprite, (selectSpriteX * 32, selectSpriteY * 32))
                
        #update the display
        pygame.display.update()
        clock.tick(60)




#call the main initialization function to start running the game
mainInit()