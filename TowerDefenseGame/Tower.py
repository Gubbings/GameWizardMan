import pygame

#This is the base class for all towers in the game it extends pygame's sprite class
class Tower(pygame.sprite.Sprite):

    pos = (0,0)    

    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.image = image  
        self.rect = self.image.get_rect()
        self.radius = 32

    #no implmentation yet for update
    def update(self, seconds):
        self.rect.topleft = self.pos
        
        


