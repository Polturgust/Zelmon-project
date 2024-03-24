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
        self.rect.inflate_ip(-5, 0)  # On réduit la taille de la hitbox du joueur pour résoudre le problème lié aux pixels entre deux images de la spritesheet
        self.lower_rect = pygame.Rect(9, 18, 12, 10)  # On définit une hitbox pour la partie inférieure du joueur pour la détection des hautes herbes / glace / plaques mouvantes
        # print("base :", self.rect.x, self.rect.y, self.rect.width, self.rect.height, 'lower: ', self.lower_rect.x, self.lower_rect.y, self.lower_rect.width, self.lower_rect.height)

        # Autres attributs
        self.velocity = 1
        self.is_moving = False  # Si le joueur se déplace
        self.on_ice = False  # Si le joueur est sur la glace
        self.slipping = False  # Si le joueur est en glisse
        self.moover_effect = None  # Si le joueur subit l'effet d'un moover et si oui sa direction

    def move(self, direction):
        """
        Permet au joueur de se déplacer dans la direction voulue

        Pré-condition :
            direction est une chaîne de caractères parmi (N, NE, E, SE, S, SW, W, NW)
        Post-conditions :
            Le PNJ se déplace dans la direction voulue
        """
        if direction == "NE":
            dest = Vector(self.pos.get()[0] + self.velocity, self.pos.get()[1] - self.velocity)  # On définit le point d'arrivée

            path = dest - self.pos  # On utilise l'overload pour calculer le vecteur de déplacement
            path.normalize()  # On normalise le vecteur pour ne pas avancer plus vite en diagonale

            self.pos += path * self.velocity  # On met à jour les coordonnées du joueur
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
            self.animation.direction = "N"  # Si on ne déplace pas en diagonale, on spécifie la direction de l'animation
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
        # On actualise l'emplacement des hitbox
        self.rect.x, self.rect.y = self.pos.get()
        self.lower_rect.x, self.lower_rect.y = self.pos.get()[0] + 7, self.pos.get()[1] + 18
        # print("base :", self.rect.x, self.rect.y, self.rect.width, self.rect.height, 'lower: ', self.lower_rect.x, self.lower_rect.y, self.lower_rect.width, self.lower_rect.height)

    def update(self):
        """
        Met à jour l'animation du joueur à l'écran selon son état :
            - Si le joueur ne marche pas, on définit une image statique selon la direction de son dernier déplacement
            - Si le joueur bouge, on fait appel à la classe Animation pour faire défiler la Spritesheet correspondant à la direction du mouvement
        """
        # pygame.draw.rect(self.game.screen.get_display(), (255, 0, 0), self.lower_rect)
        if self.is_moving and not self.slipping:  # Si le joueur se déplace normalement
            self.animation.set_frame_interval(8)
            self.animation.update(1)
            self.image = self.animation.get_current_image()
            self.velocity = 1
        elif self.is_moving and self.slipping:  # Si le joueur se déplace et glisse sur de la glace
            self.animation.set_frame_interval(32)
            self.animation.update(1)
            self.image = self.animation.get_current_image()
            self.velocity = 2
        else:  # Sinon, on affiche l'image qui correspond à la direction vers laquelle le joueur regarde
            if self.animation.direction == "N":
                self.image = pygame.image.load("assets/Spritesheets/Link/Idle-North_Link.png")
            elif self.animation.direction == "E":
                self.image = pygame.transform.flip(pygame.image.load("assets/Spritesheets/Link/Idle-West_Link.png"), True, False)
            elif self.animation.direction == "S":
                self.image = pygame.image.load("assets/Spritesheets/Link/Idle-South_Link.png")
            elif self.animation.direction == "W":
                self.image = pygame.image.load("assets/Spritesheets/Link/Idle-West_Link.png")

    def set_coordonnees(self, x, y):
        """
        Fonction qui permet de définir les coordonnées du joueur

        Pré-conditions :
            x et y sont des nombres
        Post_conditions :
            L'attribut est actualisé
        """
        self.pos = Vector(x, y)

    def get_ice_status(self):
        """
        Renvoie True si le joueur est sur de la glace, False sinon
        """
        return self.on_ice

    def set_ice_status(self, boolean):
        """
        Permet de définir si le joueur est sur de la glace

        Pré-conditions :
            boolean vaut True ou False
        Post_conditions :
            L'attribut est actualisé
        """
        self.on_ice = boolean

    def get_slipping_status(self):
        """
        Renvoie True si le joueur glisse sur de la glace, False sinon
        """
        return self.slipping

    def set_slipping_status(self, boolean):
        """
        Permet de définir si le joueur glisse sur de la glace

        Pré-conditions :
            boolean vaut True ou False
        Post_conditions :
            L'attribut est actualisé
        """
        self.slipping = boolean

    def set_moving_status(self, boolean):
        """
        Permet de définir si le joueur se déplace

        Pré-conditions :
            boolean vaut True ou False
        Post_conditions :
            L'attribut est actualisé
        """
        self.is_moving = boolean

    def set_moover_effect(self, dir):
        """
        Permet de définir si le joueur est sur une plaque mouvante et sa direction

        Pré-conditions :
             dir correspond à une direction de mouvement ou None si le joueur n'est pas sur une plaque
        Post_conditions :
             L'attribut est actualisé
        """
        self.moover_effect = dir

    def get_moover_effect(self):
        """
        Renvoie la direction de la dernière plaque touchée si le joueur en subit l'effet, None sinon
        """
        return self.moover_effect
