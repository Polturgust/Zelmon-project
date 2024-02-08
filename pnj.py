import pygame

from vector import Vector
from animation import Animation
from spritesheet import SpriteSheet


# On crée une classe PNJ qui sert de "moule" commun à tous nos PNJs. Une "super classe".
class PNJ(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        super().__init__()

        self.velocity = None
        self.pos = None

    def move(self, direction):
        """
        Fonction qui permet aux PNJs de se déplacer dans la direction voulue, au même titre que le joueur
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

    def update(self, animation, step):
        """
        Fonction qui met à jour l'animation du PNJ à l'écran
        """
        animation.update(step)
        return animation.get_current_image()


# On crée une classe enfant qui est spécifique aux chats et qui dépend de la classe PNJ.
class GreyCat(PNJ):
    def __init__(self, game, x, y):
        self.game = game
        super().__init__(self.game)

        # On définit l'emplacement du chat
        self.pos = Vector(x, y)

        # On définit la vitesse des chats
        self.velocity = 1

        # On définit ses animations
        self.animation = Animation(idle=SpriteSheet("assets/Spritesheets/chat/grey_walking_west.png").images(1, 8))
        self.animation.direction = None

        # On récupère son image
        self.image = SpriteSheet("assets/Spritesheets/chat/grey_walking_west.png").images(1, 8)[0]

        # On définit sa hitbox
        self.rect = self.image.get_rect()

    def get_current_frame(self):
        """
        Fonction qui appelle la méthode update de la superclasse PNJ pour récupérer la nouvelle image
        """
        self.image = self.update(self.animation, 1)
