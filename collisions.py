import pygame
from vector import Vector


class Collisions(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y,command):
        super().__init__()
        self.width = width
        self.height = height
        self.command=command
        """
        self.image = img
        self.image.fill((255, 0, 255))
        """
        self.image=pygame.Surface((width,height),pygame.SRCALPHA)
        self.image.fill((0, 0, 0,0))
        self.rect=pygame.Rect((x,y),(width,height))
        self.x=x
        self.y=y
        self.pos = Vector(x, y)
