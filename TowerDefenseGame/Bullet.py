import pygame
import CollectionsModule

#basic class for bullets to be shot; possibly extendable for different bullet types
class Bullet(pygame.sprite.Sprite):

    #constructor
    def __init__(self, target, distanceX, distanceY):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([4,10])
        self.image = pygame.image.load("Assets/Sprites/arrow.gif")
        self.target = target
        self.distanceX = abs(distanceX)
        self.distanceY = abs(distanceY)
        self.rect = self.image.get_rect()


    #update method used for bullet tracking
    def update(self):
        target = self.target

        if(target == None):
            self.kill()
        else:
            #move the bullet towards the enemy
            #currently it just moves directly to the enemy this is temporary
            if(self.rect.x < target.rect.centerx):
                self.rect.x += 4
            elif(self.rect.x > target.rect.centerx):
                self.rect.x -= 4

            if(self.rect.y < target.rect.centery):
                self.rect.y += 4
            elif(self.rect.y > target.rect.centery):
                self.rect.y -= 4
