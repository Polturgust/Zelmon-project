import pygame

from screen import Screen
from map import Map
from player import Player
from random import randint
from vector import Vector


class Game:
    def __init__(self):
        # set the game to running
        self.running = True
        # initialise the screen
        self.screen = Screen()
        # create a player
        self.player = Player(self)
        # initialise the screen
        self.screen = Screen()
        # initialise the map
        self.map = Map(self.screen, self.player)

        # On initialise les variables pour le mouvement du joueur :
        # Son dernier mouvement (qui par défaut est un déplacement vers la droite)
        self.last_move = "E"
        # La liste des mouvements inverses, utile dans la gestion des collisions
        self.inverse = {"NW": "SE", "NE": "SW", "SW": "NE", "SE": "NW", "N": "S", "S": "N", "E": "W", "W": "E"}
        # on crée un dictionnaire qui contient les touches pressées (permet de rester appuyé sur une touche --> utile
        # pour se déplacer)
        self.pressed = dict()

        self.cooldown = 0

    def run(self):
        # Tant que le jeu tourne :
        while self.running:
            # On récupère toutes les actions de l'utilisateur
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # On ferme le jeu si l'utilisateur ferme la fenêtre
                    self.running = False
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée, on l'ajoute au dictionnaire des touches pressées
                    self.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed[
                        event.key] = False  # Si une touche est relâchée, on l'enlève du dictionnaire des touches pressées

            # Checking currently pressed keys and doing the according actions

            # Player movement
            # sans le -30 on peut sortir de l'écran je pense que c'est dû à la largeur du carré (ses coordonnées sont le point en haut à gauche)
            if self.pressed.get(pygame.K_UP) and self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[1] > 0 and \
                    self.player.pos.get()[0] < self.map.map_data.map_size[0] * 16 - 30:
                self.player.move("NE")
                self.last_move = "NE"
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_UP) and self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[1] > 0 and \
                    self.player.pos.get()[0] > 0:
                self.player.move("NW")
                self.last_move = "NW"
                if self.cooldown != 0:
                    self.cooldown -= 1

            elif self.pressed.get(pygame.K_DOWN) and self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[1] < \
                    self.map.map_data.map_size[1] * 16 - 30 and self.player.pos.get()[0] < self.map.map_data.map_size[
                0] * 16 - 30:
                self.player.move("SE")
                self.last_move = "SE"
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_DOWN) and self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[1] < \
                    self.map.map_data.map_size[1] * 16 - 30 and self.player.pos.get()[0] > 0:
                self.player.move("SW")
                self.last_move = "SW"
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_UP) and self.player.pos.get()[1] > 0:
                self.player.move("N")
                self.last_move = "N"
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_DOWN) and self.player.pos.get()[1] < self.map.map_data.map_size[1] * 16 - 30:
                self.player.move("S")
                self.last_move = "S"
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[0] > 0:
                self.player.move("W")
                self.last_move = "W"
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[0] < self.map.map_data.map_size[0] * 16:
                self.player.move("E")
                self.last_move = "E"
                if self.cooldown != 0:
                    self.cooldown -= 1

            if self.cooldown == 0:
                if self.chance_rencontre() == True:
                    self.playerinfo = self.player.pos.get()
                    self.origin = self.map.zonearr
                    self.map.switch_map("combat")
                    self.lancer_combat("Pokemon Sauvage")

            # Vérifie si le joueur est en collision avec un élément du décor
            for i in self.map.collisions:
                if self.player.rect.colliderect(i.rect) and not isinstance(i, Player):
                    # Si oui, on effectue le mouvement inverse de celui que vient d'effectuer le joueur.
                    self.player.move(self.inverse[self.last_move])

            # Vérifie si le joueur touche une zone qui doit le faire changer d'endroit
            for i in self.map.changes:
                if self.player.rect.colliderect(i.rect):
                    # Si oui, on change la carte affichée en appelant la méthode switch_map() de la classe Map avec le nom de la carte associée à la collision
                    self.map.switch_map(i.command)

            # update map
            self.map.update()

            # update player
            # if the screen still scrolls make the player appear in the center

            # self.screen.get_display().blit(self.player.image, (self.player.pos.get()))

            # update screen
            self.screen.update()
        pygame.quit()

    def chance_rencontre(self):
        for i in self.map.weeds:
            if self.player.rect.colliderect(i.rect):
                self.alearencontre = randint(0, 100)
                if self.alearencontre < 2:
                    return True
        return False

    def lancer_combat(self, name):
        self.name = name
        print(self.name + " veut se battre !")
        self.winner = 0
        while self.winner == 0 and self.running:
            self.screen.update()
            self.map.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # On ferme le jeu si l'utilisateur ferme la fenêtre
                    self.running = False
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée, on l'ajoute au dictionnaire des touches pressées
                    self.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed[
                        event.key] = False  # Si une touche est relâchée, on l'enlève du dictionnaire des touches pressées

            self.screen.get_display().blit(
                pygame.transform.scale(pygame.image.load("assets\\images\\player.jpg"), (40, 40)),
                (40, self.screen.get_display().get_size()[1] - 70))
            self.screen.get_display().blit(
                pygame.transform.scale(pygame.image.load("assets\\images\\pokemon.jpg"), (40, 40)),
                (self.screen.get_display().get_size()[0] - 70, 40))
            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render("You", False, (0, 0, 0)),
                                           (40, self.screen.get_display().get_size()[1] - 120))
            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(self.name, False, (0, 0, 0)),
                                           (self.screen.get_display().get_size()[0] - 200, 10))

            if pygame.K_a in self.pressed.keys() and self.pressed[pygame.K_a] == True:
                print(self.pressed)
                self.pressed[pygame.K_a] = False
                self.winner = 1
        self.map.switch_map(self.origin)
        self.player.pos = Vector(self.playerinfo[0], self.playerinfo[1])
        self.cooldown = 120
        return None
