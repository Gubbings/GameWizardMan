import pygame
import CollectionsModule

#basic class for bullets to be shot; possibly extendable for different bullet types
class Bullet(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([4,10])
        self.image.fill(CollectionsModule.Color.black)
        
        self.rect = self.image.get_rect()

    #bullet moves down the screen right now
    #TODO: track enemies and shoot them
    def update(self):
        self.rect.y += 3