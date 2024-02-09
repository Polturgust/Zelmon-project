import pygame

from vector import Vector
from animation import Animation
from spritesheet import SpriteSheet


class PNJ(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game

        super().__init__()

        # Coordonnées du joueur (au centre par défaut)
        self.pos = Vector(200, 220)

        # Autres attributs
        self.velocity = 1
        self.is_moving = False

    def move(self, direction):
        """
        Permet au PNJ de se déplacer dans la direction voulue au même titre que le joueur

        Pré-condition :
            direction est une chaîne de caractères parmi (N, NE, E, SE, S, SW, W, NW)
        Post-conditions :
            Le PNJ se déplace dans la direction voulue
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
        Met à jour l'animation du PNJ à l'écran an faisant appel à la classe Animation pour faire défiler la Spritesheet

        Post-condition :
            self.image contient désormais la nouvelle image à afficher
        """
        self.animation.update(1)
        self.image = self.animation.get_current_image()


class GreyCat(PNJ):
    def __init__(self, game, x, y):
        # Coordonnées du joueur (au centre par défaut)
        super().__init__(game)
        self.pos = Vector(x, y)

        # On définit ses animations
        self.animation = Animation(idle=SpriteSheet("assets/Spritesheets/chat/grey_walking_west.png").images(1, 8))
        self.animation.frame_interval = 24
        self.animation.direction = None

        # On récupère son image de base
        self.image = pygame.image.load("assets/Spritesheets/chat/grey_walking_west_single.png").convert_alpha()

        self.rect = self.image.get_rect()

