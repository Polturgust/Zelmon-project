import pygame
from vector import Vector


class Collisions(pygame.sprite.Sprite):

    def __init__(self, width, height, img, x, y):
        super().__init__()
        self.width = width
        self.height = height
        self.img = img
        self.img.fill("WHITE")
        self.rect=self.img.get_rect()
        self.x=x
        self.y=y
        self.pos = Vector(x, y)

    def update(self):
        pygame.draw.rect(self.img,"WHITE",[self.x,self.y,self.width,self.height])
        print(self.x,self.y)
