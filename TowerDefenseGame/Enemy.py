import pygame
import Player

#this class represents a single enemy in the game. It inherits from the pygame
#Sprite object and includes parameters for pathfinding and collision
class Enemy(pygame.sprite.Sprite):

    #data members for an enemy
    bulletGroup = None
    towerGroup = None

    def __init__(self, nodesInPath, image, playerBase):
        pygame.sprite.Sprite.__init__(self, self.groups)

        #position of the sprite [x,y]
        self.pos = []

        #enemy health
        self.health = 10

        #next node to advance to
        self.nodeIndex = 0

        #desired final position of the enemy
        self.playerBase = playerBase

        #amount of health taken when the enemy reaches the base
        self.damage = -2

        #radius used for collision
        self.radius = 32
        self.image = image
        self.rect = self.image.get_rect()

        #nodes used for pathfinding
        self.nodeList = nodesInPath
        self.pos.append(nodesInPath[0].x)
        self.pos.append(nodesInPath[0].y)
        self.rect.topleft = self.pos

    #update method runs every time the sprite group calls update
    def update(self):

        #check if a bullet has collided with the enemy
        if(pygame.sprite.spritecollide(self, self.bulletGroup, 1)):
           self.health -= 2

        #check if the enemy reached the player base
        if(self.pos[0] + 2 >= self.playerBase.x and self.pos[0] + 2 <= self.playerBase.x + self.playerBase.width):
            if(self.pos[1] + 2 >= self.playerBase.y and self.pos[1] + 2 <= self.playerBase.y + self.playerBase.height):
                #reduce player health when the enemy reaches the base
                Player.health += self.damage

                #remove the enemy
                for tower in self.towerGroup:
                    if(tower.target == self):
                        tower.target = None
                self.kill()

        #kill the enemy when its health is 0 or less
        if(self.health <= 0):
            Player.gold += 5
            for tower in self.towerGroup:
                if(tower.target == self):
                    tower.target = None
            Player.enemiesKilled += 1
            deathSound = pygame.mixer.Sound('death.wav')
            deathSound.play()
            self.kill()



        nodes = self.nodeList
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
