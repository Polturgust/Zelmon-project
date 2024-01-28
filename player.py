import pygame
from screen import Screen
from vector import Vector


class Player:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

        # Image du joueur
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        # Coordonnées du joueur
        self.x = 0
        self.y = 0
        self.pos = Vector(self.x, self.y)

        # Autres attributs
        self.velocity = 1
        self.is_moving = False

    def move(self, direction):
        """
        Permet au joueur de se déplacer dans la direction voulue
        """
        if direction == "NE":
            dest = Vector(self.pos.get()[0] + self.velocity, self.pos.get()[1] - self.velocity)

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity
        elif direction == "NW":
            dest = Vector(self.pos.get()[0] - self.velocity, self.pos.get()[1] - self.velocity)

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity
        elif direction == "SE":
            dest = Vector(self.pos.get()[0] + self.velocity, self.pos.get()[1] + self.velocity)

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity
        elif direction == "SW":
            dest = Vector(self.pos.get()[0] - self.velocity, self.pos.get()[1] + self.velocity)

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity
        elif direction == "N":
            dest = Vector(self.pos.get()[0], self.pos.get()[1] - self.velocity)

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity
        elif direction == "S":
            dest = Vector(self.pos.get()[0], self.pos.get()[1] + self.velocity)

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity
        elif direction == "W":
            dest = Vector(self.pos.get()[0] - self.velocity, self.pos.get()[1])

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity
        elif direction == "E":
            dest = Vector(self.pos.get()[0] + self.velocity, self.pos.get()[1])

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity

    def update(self):
        """
        Affiche le joueur à l'écran
        """
        self.screen.get_display().blit(self.image, self.pos.tuple)
