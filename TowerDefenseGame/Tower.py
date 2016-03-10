import pygame
import Bullet


#This is the base class for all towers in the game it extends pygame's sprite class
class Tower(pygame.sprite.Sprite):

    pos = (-100, -100)   
    fireRate = 10
    bulletTick = 0 
    target = None
    bullets = []

    def __init__(self, image, pos, target):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.image = image  
        self.rect = self.image.get_rect()
        self.radius = 32
        self.fireRate = 60
        self.bulletTick = 0
        self.target = target

    #update method runs every time the sprite group calls update
    def update(self):
        self.rect.topleft = self.pos
        
        if self.target != None:
            if self.bulletTick == self.fireRate:
                bullet = Bullet.Bullet(self.target, self.rect.x - self.target.rect.x, self.rect.y - self.target.rect.y)
                bullet.rect.x = self.rect.x
                bullet.rect.y = self.rect.y
                self.bulletTick = 0
                self.bullets.append(bullet)
            self.bulletTick = self.bulletTick + 1
        else:
            for bullet in self.bullets:
                bullet.target = None
        
        


