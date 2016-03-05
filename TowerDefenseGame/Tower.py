import pygame

#This is the base class for all towers in the game it extends pygame's sprite class
class Tower(pygame.sprite.Sprite):

    towerImg = pygame.Surface((32,32))
    towerImg.blit(pygame.image.load("Assets/towerTemp.gif"), (0,0))
    pos = (0,0)
    img = pygame.image.load("Assets/towerTemp.gif")
    

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Tower.towerImg 
        self.rect = self.image.get_rect()
        self.radius = 32

    #no implmentation yet for update
    def update(self, seconds):
        self.rect.center = pygame.mouse.get_pos()
        
        


