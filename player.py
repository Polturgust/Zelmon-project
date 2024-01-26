import pygame
from screen import Screen


class Player:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def move(self, direction):
        """
        Permet au joueur de se déplacer dans la direction voulue
        """
        if direction == "up":
            self.rect.y -= 5
        elif direction == "down":
            self.rect.y += 5
        elif direction == "right":
            self.rect.x += 5
        elif direction == "left":
            self.rect.x -= 5

    def update(self):
        """
        Affiche le joueur à l'écran
        """
        self.screen.get_display().blit(self.image, self.rect)
