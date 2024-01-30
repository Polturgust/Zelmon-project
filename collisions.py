import pygame
from vector import Vector


class Collisions(pygame.sprite.Sprite):

    def __init__(self, width, height, img, x, y):
        super().__init__()
        self.width = width
        self.height = height
        self.image = img
        self.image.fill((255, 255, 0))
        self.rect=self.image.get_rect()
        self.x=x
        self.y=y
        self.pos = Vector(x, y)
