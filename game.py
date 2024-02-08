import pygame
from random import randint

from screen import Screen
from map import Map
from player import Player
from combat import Combat
from pnj import *


class Game:
    def __init__(self):
        # set the game to running
        self.running = True
        # initialise the screen
        self.screen = Screen()
        # create a player
        self.player = Player(self)
        # initialise the screen
        self.map = Map(self.screen, self.player)

        # On tente de créer un chat
        self.map.add_pnj(GreyCat(self, 200, 240))

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
                self.player.is_moving = True
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_UP) and self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[1] > 0 and \
                    self.player.pos.get()[0] > 0:
                self.player.move("NW")
                self.last_move = "NW"
                self.player.is_moving = True
                if self.cooldown != 0:
                    self.cooldown -= 1

            elif self.pressed.get(pygame.K_DOWN) and self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[1] < \
                    self.map.map_data.map_size[1] * 16 - 30 and self.player.pos.get()[0] < self.map.map_data.map_size[0] * 16 - 30:
                self.player.move("SE")
                self.last_move = "SE"
                self.player.is_moving = True
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_DOWN) and self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[1] < \
                    self.map.map_data.map_size[1] * 16 - 30 and self.player.pos.get()[0] > 0:
                self.player.move("SW")
                self.last_move = "SW"
                self.player.is_moving = True
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_UP) and self.player.pos.get()[1] > 0:
                self.player.move("N")
                self.last_move = "N"
                self.player.is_moving = True
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_DOWN) and self.player.pos.get()[1] < self.map.map_data.map_size[1] * 16 - 30:
                self.player.move("S")
                self.last_move = "S"
                self.player.is_moving = True
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[0] > 0:
                self.player.move("W")
                self.last_move = "W"
                self.player.is_moving = True
                if self.cooldown != 0:
                    self.cooldown -= 1
            elif self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[0] < self.map.map_data.map_size[0] * 16:
                self.player.move("E")
                self.last_move = "E"
                self.player.is_moving = True
                if self.cooldown != 0:
                    self.cooldown -= 1
            else:
                self.player.is_moving = False

            if self.cooldown == 0:
                if self.chance_rencontre() is True:
                    self.origin = self.map.zonearr
                    self.map.switch_map("combat")
                    self.pressed = {}
                    self.combat = Combat("Pokémon sauvage", self.screen, self.player, self.map, self.origin)
                    if self.combat.lancer_combat() is False:
                        self.running = False
                    self.cooldown = 120

            # Vérifie si le joueur est en collision avec un élément du décor
            for i in self.map.collisions:
                if self.player.rect.colliderect(i.rect) and not isinstance(i, Player):
                    # Si oui, on effectue deux fois le mouvement inverse de celui que vient d'effectuer le joueur puis une fois le même.
                    # De cette façon, le joueur ne peut avancer et l'animation ne le montre pas comme allant dans le sens opposé à celui de la collision.
                    self.player.move(self.inverse[self.last_move])
                    self.player.move(self.inverse[self.last_move])
                    self.player.move(self.last_move)



            # Vérifie si le joueur touche une zone qui doit le faire changer d'endroit
            for i in self.map.changes:
                if self.player.rect.colliderect(i.rect):
                    # Si oui, on change la carte affichée en appelant la méthode switch_map() de la classe Map avec le nom de la carte associée à la collision
                    self.map.switch_map(i.command)

            # update map
            self.map.update()

            # update player animation
            self.player.update()

            # update pnjs animation
            for pnj in self.map.pnjs_list:
                pnj.get_current_frame()
                # self.screen.get_display().blit(pnj.image, pnj.pos.get())

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

