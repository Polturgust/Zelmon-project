import pygame

from vector import Vector
from animation import Animation
from spritesheet import SpriteSheet


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game

        super().__init__()

        # Coordonnées du joueur (au centre de l'écran par défaut)
        self.pos = Vector(300, 240)

        # On définit les sprites
        self.animation = Animation(SpriteSheet("assets/Spritesheets/Link/Walking-North_Link.png").images(1, 10), SpriteSheet("assets/Spritesheets/Link/Walking-South_Link.png").images(1, 10), SpriteSheet("assets/Spritesheets/Link/Walking-West_Link.png").images(1, 10))
        self.image = pygame.image.load("assets/Spritesheets/Link/Idle-South_Link.png").convert_alpha()
        self.bottom_link = pygame.image.load("assets/Spritesheets/Link/bottom_Link.png").convert_alpha()

        # Hitbox
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-5, 0)  # On réduit la taille de la hitbox du joueur pour résoudre le problème lié aux pixels entre deux frames
        # self.rect.move_ip(0, 60)  # Souhaite déplacer la hitbox vers le bas pour que seuls les pieds aient des collisions

        # Autres attributs
        self.velocity = 1
        self.is_moving = False

    def move(self, direction):
        """
        Permet au joueur de se déplacer dans la direction voulue

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
        Met à jour l'animation du joueur à l'écran selon son état :
            - Si le joueur ne marche pas, on définit une image statique selon la direction de son dernier déplacement
            - Si le joueur bouge, on fait appel à la classe Animation pour faire défiler la Spritesheet correspondant à la direction du mouvement
        """
        if self.is_moving:  # Si le joueur se déplace
            self.animation.update(1)
            self.image = self.animation.get_current_image()
        else:
            if self.animation.direction == "N":
                self.image = pygame.image.load("assets/Spritesheets/Link/Idle-North_Link.png")
            elif self.animation.direction == "E":
                self.image = pygame.transform.flip(pygame.image.load("assets/Spritesheets/Link/Idle-West_Link.png"), True, False)
            elif self.animation.direction == "S":
                self.image = pygame.image.load("assets/Spritesheets/Link/Idle-South_Link.png")
            elif self.animation.direction == "W":
                self.image = pygame.image.load("assets/Spritesheets/Link/Idle-West_Link.png")
        # pygame.draw.rect(self.game.screen.get_display(), (255, 0, 0), self.rect)
