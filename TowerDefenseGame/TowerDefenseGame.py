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
import Player

#clock for controlling the FPS
clock = pygame.time.Clock()

#screen parameters
playableWidth = 704
screenWidth = 896
screenHeight = 576
screenSize = screenWidth, screenHeight
mainSurface = pygame.display.set_mode(screenSize)

#image for the tile selection sprite
tileSelectSprite = pygame.image.load("Assets/selectSprite.gif")

#tiled map
map1 = load_pygame("Assets/Maps/testMap.tmx")

#music enabled flag
enableMusic = True


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
def text_objects(text, font, color):
    #render the text with a color of black
    textSurface = font.render(text, True, color)
    return textSurface


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
        textSurf = text_objects(msg, smallText, CollectionsModule.Color.black)
        textRect = textSurf.get_rect()
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
    #delay for 100 milliseconds so the user doesnt place a tower with the click from hitting play
    pygame.time.delay(100)

    #configure the gamepad controller if one is connected
    controller = None
    if(pygame.joystick.get_count() > 0):
        #get the first connected joystick     
        controller = pygame.joystick.Joystick(0)   
        controller.init()             

    #black background
    mainSurface.fill(CollectionsModule.Color.black)

    Player.health = 100
    Player.gold = 25

    #get the object group with our AI path nodes
    path = map1.get_layer_by_name("EnemyPath")
    nodes = []

    #add each node to the list of nodes
    for node in path:
        nodes.append(node)

    #sort the list of path nodes to ensure they are in the proper order
    nodes.sort()

    #get the second path for enemies and apply the same process as path 1
    path2 = map1.get_layer_by_name("EnemyPath2")
    nodes2 = []

    for node in path2:
        nodes2.append(node)

    nodes2.sort

    #get the object group with that marks the buildable surface area
    buildableArea = map1.get_layer_by_name("Buildable")    
    buildableList = []
    for area in buildableArea:        
        buildableList.append(area)

    #get the object group that marks the players base camp
    baseCamp = map1.get_layer_by_name("Base")

    #player's base is a list however it is expected to have only 1 object
    baseCampList = []
    for base in baseCamp:
        baseCampList.append(base)
    playerBase = baseCampList[0]

    #group of tower sprites
    towerList = pygame.sprite.Group()
    #group of bullet sprites
    bulletList = pygame.sprite.Group()       
    #group of enemy sprites
    enemyList = pygame.sprite.Group()

    #setup static variables on the sprite classes
    Bullet.Bullet.groups = bulletList

    Enemy.Enemy.groups = enemyList
    Enemy.Enemy.towerGroup = towerList
    Enemy.Enemy.bulletGroup = bulletList

    Tower.Tower.groups = towerList
    Tower.Tower.enemyGroup = enemyList   

    

    #variables for controlling spawn rate of enemies 
    enemyCount = 0
    spawnTick = 0
    spawnRate = 180

    #create an enemy
    enemyGif = pygame.transform.scale(pygame.image.load("Assets/Sprites/enemy1.png"), (32,32))    
    enemy = Enemy.Enemy(nodes, enemyGif, playerBase)
    
    #create a tower
    towerGif = pygame.image.load("Assets/Sprites/towerTemp.gif")    
    
    #position of the tile selection sprite    
    selectSpriteX = 0
    selectSpriteY = 0
    #create a new user event for tracking joystick movement        
    JOYSTICK_MOVE_EVENT = pygame.USEREVENT + 1

    #click event
    MOUSE_CLICK_EVENT = pygame.USEREVENT + 2
    #fire a click event every 100 milliseconds
    pygame.time.set_timer(MOUSE_CLICK_EVENT, 100)

    #check if we have a controller before performing anything that pertains to the controller
    if(controller != None):            
        #get the bounds of the tiled map
        xBound = playableWidth
        yBound = screenHeight
        
        #time between JOYSTICK_MOVE_EVENTs
        timeBetweenEvents = 250

        #cause a joystick move event every 't' milliseconds where 't' is defined as timeBetweenEvents
        pygame.time.set_timer(JOYSTICK_MOVE_EVENT, timeBetweenEvents)


    #flag to tell if the selection area is in the playable area or not
    outOfBounds = False

    #game loop
    while True:
        #check for pygame events                                      
        for event in pygame.event.get():                        
            if event.type == pygame.QUIT: 
                exit()

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

            if event.type == MOUSE_CLICK_EVENT:                
                #mouse position
                mouse = pygame.mouse.get_pos()

                #get state of the left mouse button
                leftMouseDown = pygame.mouse.get_pressed()[0] == 1
                
                #dont update selection sprite when the mouse is out of playable area
                if(not outOfBounds):
                    selectSpriteX = int(mouse[0] / 32)                
                    selectSpriteY = int(mouse[1] / 32)

                if(mouse[0] > playableWidth):
                    selectSpriteX = playableWidth / 32 - 1
                    outOfBounds = True
                else:
                    outOfBounds = False
                
                #if user clicks attempt to place a tower
                if(leftMouseDown):
                    #check if user is placing a tower
                    if(not outOfBounds):
                        for area in buildableList:                        
                            #make sure the selection is horizontally and vertically in a buildable area
                            if(selectSpriteX * 32 + 2 > area.x and selectSpriteX * 32 + 2< area.x + area.width):
                                if(selectSpriteY * 32 + 2 > area.y and selectSpriteY * 32 + 2 < area.y + area.height):                            
                                    #make sure there is not a tower already in the selected spot
                                    if(len(towerList) > 0):
                                        for tower in towerList:
                                            if(selectSpriteX * 32 != tower.pos[0] or selectSpriteY * 32 != tower.pos[1]):
                                                #does user have enough gold
                                                if(Player.gold >= 5):
                                                    #spawn a new tower
                                                    Tower.Tower(towerGif, (selectSpriteX * 32, selectSpriteY * 32))
                                                    print("tower")
                                                    break
                                    else:                                        
                                        Tower.Tower(towerGif, (selectSpriteX * 32, selectSpriteY * 32))
                                        print("tower")
                                        break


            #check if user clicked the 'A' button
            if event.type == pygame.JOYBUTTONDOWN:
                if controller.get_button(0):                                        
                    #TODO: tower targets is currently hard coded we will base it on proximity in the future                                  
                    #check if user is placing a tower
                    if(not outOfBounds):
                        for area in buildableList:                        
                            #make sure the selection is horizontally and vertically in a buildable area
                            if(selectSpriteX * 32 + 2 > area.x and selectSpriteX * 32 + 2< area.x + area.width):
                                if(selectSpriteY * 32 + 2 > area.y and selectSpriteY * 32 + 2 < area.y + area.height):                            
                                    #make sure there is not a tower already in the selected spot
                                    if(len(towerList) > 0):
                                        for tower in towerList:
                                            if(selectSpriteX * 32 != tower.pos[0] or selectSpriteY * 32 != tower.pos[1]):
                                                #does user have enough gold
                                                if(Player.gold >= 5):
                                                    #spawn a new tower
                                                    Tower.Tower(towerGif, (selectSpriteX * 32, selectSpriteY * 32))
                                                    print("tower")
                                                    break
                                    else:                                        
                                        Tower.Tower(towerGif, (selectSpriteX * 32, selectSpriteY * 32))
                                        print("tower")
                                        break


        #display all of the tiles from the tiled map
        for layer in map1.layers:
            #we have marked object layers as invisible because they have no images 
            #only get the layers that are visible
            if layer.visible:
                for x, y, image in layer.tiles():                
                    mainSurface.blit(image, (32 * x, 32 * y))                  

        #spawn new enemies based on the spawn rate
        if(spawnTick >= spawnRate):
            Enemy.Enemy(nodes, enemyGif, playerBase)
            enemyCount += 1

            #after 15 enemies have spawned start spawning extra from the second path
            if(enemyCount > 15):
                Enemy.Enemy(nodes2, enemyGif, playerBase)
                enemyCount += 1

            spawnTick = 0       
        spawnTick = spawnTick + 1


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
                

        #display the players health
        font = pygame.font.Font("Assets/Fonts/EdselFont.ttf", 20)
        textSurf = text_objects("Health: " + str(Player.health), font, CollectionsModule.Color.white)
        textRect = textSurf.get_rect()
        textRect.center = ((screenWidth - playableWidth) / 2 + playableWidth), (screenHeight * 0.05)
        mainSurface.blit(textSurf, textRect)

        textSurf = text_objects("Gold: " + str(Player.gold), font, CollectionsModule.Color.white)
        textRect = textSurf.get_rect()
        textRect.center = ((screenWidth - playableWidth) / 2 + playableWidth), (screenHeight * 0.1)
        mainSurface.blit(textSurf, textRect)


        if(Player.health <= 0):
            gameOver()

        #update the display
        pygame.display.update()
        clock.tick(60)




#function to execute when the player wins or loses the level
def gameOver():

    while True:
        #check for pygame quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit()
        
        font = pygame.font.Font("Assets/Fonts/EdselFont.ttf", 40)
        white = CollectionsModule.Color.white
        red = CollectionsModule.Color.red

        #display a button to return to the main title screen on win/loss
        #currently they both perform the same function just with different text
        if(Player.health <= 0):           
            button("Game Over", playableWidth / 2, screenHeight / 2, 100, 50, white, red, mainInit)            
        else:
            button("Level Complete", playableWidth / 2, screenHeight / 2, 100, 50, white, red, mainInit)

        #update the display
        pygame.display.update()
        clock.tick(60)



#call the main initialization function to start running the game
mainInit()