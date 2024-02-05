import pygame
from screen import Screen
from vector import Vector
from animation import Animation


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        # self.screen = screen

        super().__init__()

        # Coordonnées du joueur (au centre par défaut)
        # self.x = 300  # self.screen.dimensions[0] // 2
        # self.y = 240  # self.screen.dimensions[1] // 2
        self.pos = Vector(300, 240)

        # On définit les sprites
        self.animation = Animation()
        self.image = self.animation.get_current_image()

        # Hitbox
        self.rect = self.image.get_rect()

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
            self.animation.direction = "N"
        elif direction == "S":
            dest = Vector(self.pos.get()[0], self.pos.get()[1] + self.velocity)

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity
            self.animation.direction = "S"
        elif direction == "W":
            dest = Vector(self.pos.get()[0] - self.velocity, self.pos.get()[1])

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity
            self.animation.direction = "W"
        elif direction == "E":
            dest = Vector(self.pos.get()[0] + self.velocity, self.pos.get()[1])

            path = dest - self.pos
            path.normalize()

            self.pos += path * self.velocity
            self.animation.direction = "E"
        self.rect.x, self.rect.y = self.pos.get()

    def update(self):
        """
        Met à jour l'animation du joueur à l'écran
        """
        if self.is_moving:  # Si le joueur se déplace
            self.animation.frame_rate = 8
            self.animation.update(1)
            self.image = self.animation.get_current_image()
        else:
            self.animation.frame_rate = 24
            self.animation.update(3)
            self.image = self.animation.get_current_image()
