import pygame

#this class represents a single enemy in the game. It inherits from the pygame
#Sprite object and includes parameters for pathfinding and collision
class Enemy(pygame.sprite.Sprite):
    
    #data members for an enemy
    health = 10
    pos = [0,0]
    nodes = []
    nodeIndex = 1
    bulletGroup = None
    towerGroup = None
         
    def __init__(self, nodesInPath, image):
        pygame.sprite.Sprite.__init__(self, self.groups)        
        self.image = image  
        self.rect = self.image.get_rect()
        self.radius = 32
        self.nodes = nodesInPath
        self.pos[0] = nodesInPath[0].x
        self.pos[1] = nodesInPath[0].y
        self.rect.topleft = self.pos     
    
    #update method runs every time the sprite group calls update
    def update(self):

        #check if a bullet has collided with the enemy
        if(pygame.sprite.spritecollide(self, self.bulletGroup, 1)):
           self.health -= 1
        
        #kill the enemy when its health is 0 
        if(self.health <= 0):                        
            for tower in self.towerGroup:
                if(tower.target == self):
                    tower.target = None
            self.kill()
        
        nodes = self.nodes        
        #check the npcs position relative to its next node
        if (self.nodeIndex < len(nodes)) and (self.pos[0] != nodes[self.nodeIndex].x or self.pos[1] != nodes[self.nodeIndex].y):            
            #move the npc towards the next node - up/down/left/right
            if (self.pos[0] < nodes[self.nodeIndex].x): 
                self.pos[0] += 1
            elif (self.pos[0] > nodes[self.nodeIndex].x):
                self.pos[0] -= 1
            elif (self.pos[1] < nodes[self.nodeIndex].y):
                self.pos[1] += 1
            else:
                self.pos[1] -= 1 
        else:
            self.nodeIndex += 1


        self.rect.topleft = self.pos


