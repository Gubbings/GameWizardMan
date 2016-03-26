import pygame
import Bullet
import Player

#This is the base class for all towers in the game it extends pygame's sprite class
class Tower(pygame.sprite.Sprite):

    enemyGroup = None

    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect()
        self.radius = 32
        self.bullets = []
        self.fireRate = 60
        self.bulletTick = 0
        self.cost = 5
        self.target = None

        #enlarge the collision rectangle
        self.rect = self.rect.inflate(150, 150)
        Player.gold -= self.cost

    #update method runs every time the sprite group calls update
    def update(self):
        self.rect.topleft = self.pos

        #check if we have a target
        if self.target != None:
            #fire a bullet based on the fire rate
            if self.bulletTick == self.fireRate:
                bullet = Bullet.Bullet(self.target, self.rect.x - self.target.rect.x, self.rect.y - self.target.rect.y)
                bullet.rect.x = self.rect.x
                bullet.rect.y = self.rect.y
                self.bulletTick = 0
                self.bullets.append(bullet)
            self.bulletTick = self.bulletTick + 1

            #when the target moves out of range reset target to none
            if(not pygame.sprite.collide_rect(self, self.target)):
                self.target = None
        else:
            #remove any bullets in flight to the previous target
            for bullet in self.bullets:
                bullet.target = None

            #check for collision with an enemy to find a target
            collisions = pygame.sprite.spritecollide(self, self.enemyGroup, False)
            if(len(collisions) > 0):
                self.target = collisions[0]
                              
