import pygame
from pytmx.util_pygame import load_pygame
import CollectionsModule
import Tower

#global variables
clock = pygame.time.Clock()
screenWidth = 800
screenHeight = 700
screenSize = screenWidth, screenHeight
mainSurface = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
tileSelectSprite = pygame.image.load("Assets/selectSprite.gif")


#maps
map1 = load_pygame('Assets/Maps/testMap.tmx')

#function used for primary initialization 
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
        button("Quit", screenWidth / 2 - 50, 575, 100, 50, CollectionsModule.Color.white, CollectionsModule.Color.red, exit)
        
        #update entire display 
        pygame.display.flip()

        #60fps or lower
        clock.tick(60)





#----------------------------------------------------------------------
#   MAIN GAME LOOP
#----------------------------------------------------------------------
def mainGameLoop():    

    controller = None
    if(pygame.joystick.get_count() > 0):
        #get the first connected joystick     
        controller = pygame.joystick.Joystick(0)   
        #controller.init()             

    #black background
    mainSurface.fill(CollectionsModule.Color.black)


    #get the object group with our AI path nodes
    path = map1.get_layer_by_name("EnemyPath")

    nodes = []
    # iterate through nodes in the object group:
    for node in path:
        nodes.append(node)

    nodes.sort()

    #the npc must start at the first node
    npcX = nodes[0].x
    npcY = nodes[0].y
    
    #track the node the npc is moving towards
    nodeIndex = 1
        


    #group of tower sprites
    towerList = pygame.sprite.Group()
    Tower.Tower.groups = towerList
    towerGif = pygame.image.load("Assets/towerTemp.gif")
    tower = Tower.Tower(towerGif, (32, 32))  
    bg = pygame.Surface((32,32))
    bg.fill((0,0,0))


    #position of the tile selection sprite    
    selectSpriteX = 0
    selectSpriteY = 0

    #get the bounds of the tiled map
    xBound = 0
    yBound = 0
    for x, y, image in map1.layers[0].tiles():                
        if(x > xBound):
            xBound = x
        if(y > yBound):
            yBound = y


    #create a new user event for tracking joystick movement
    JOYSTICK_MOVE_EVENT = pygame.USEREVENT+1
    t = 500

    if(controller != None):    
        #cause a joystick move event every 500 milliseconds
        pygame.time.set_timer(JOYSTICK_MOVE_EVENT, t)

    #game loop
    while True:                                 
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

        #display all of the tiles from the tiled map
        for layer in map1.layers:
            #we have marked object layers as invisible because they have no images 
            #only get the layers that are visible
            if layer.visible:
                for x, y, image in layer.tiles():                
                    mainSurface.blit(image, (32 * x, 32 * y))                  

        towerList.clear(mainSurface, bg)
        towerList.draw(mainSurface)
        towerList.update(1)

        #display the tile selection sprite
        mainSurface.blit(tileSelectSprite, (selectSpriteX * 32, selectSpriteY * 32))

                
        #draw the npc
        npc = pygame.draw.rect(mainSurface, CollectionsModule.Color.red, (npcX, npcY, 32, 32))

        #check the npcs position relative to its next node
        if (nodeIndex < len(nodes)) and (npc.x != nodes[nodeIndex].x or npc.y != nodes[nodeIndex].y):            
            #move the npc towards the next node - up/down/left/right
            if (npcX < nodes[nodeIndex].x): 
                npcX += 1
            elif (npcX > nodes[nodeIndex].x):
                npcX -= 1
            elif (npcY < nodes[nodeIndex].y):
                npcY += 1
            else:
                npcY -= 1 
        else:
            nodeIndex += 1



#        pygame.draw.rect(mainSurface, CollectionsModule.Color.red, (nodes[nodeIndex].x, nodes[nodeIndex].y, 32, 32))
#        if pygame.time.get_ticks() > 1000 * nodeIndex and nodeIndex < len(nodes) - 1:
#            nodeIndex += 1


#        for node in nodes:
#            print(node.properties["NodeIndex"])


        #update the display
        pygame.display.update()
        clock.tick(60)




#call the first initialization function
mainInit()