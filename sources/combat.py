import pygame
from vector import Vector


class Combat:
    def __init__(self, game, screen, player, map, origin,save):
        self.game = game
        self.screen = screen
        self.player = player
        self.running = True
        self.map = map
        self.pressed = {}
        self.origin = origin
        self.save=save

    def combat_sauvage(self, id_poke_adv):
        """
        Fonction qui lance un combat.
        Un combat prend fin quand un des deux Pokémon est K.O ou si le joueur fuit en appuyant sur "a"
        """
        self.info_espece=self.game.save_selected.get_info_espece(id_poke_adv)
        print(self.info_espece["Nom"] + " veut se battre !")

        self.winner = 0
        self.pv = self.info_espece["PV"]

        while self.winner == 0 and self.running:
            self.screen.update()
            self.map.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # On ferme le jeu si l'utilisateur ferme la fenêtre
                    self.running = False
                    return False
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée, on l'ajoute au dictionnaire des touches pressées
                    self.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False  # Si une touche est relâchée, on l'enlève du dictionnaire des touches pressées

            # On affiche le pokémon du joueur
            self.screen.get_display().blit(
                pygame.transform.scale(pygame.image.load("assets\\images\\player.jpg"), (40, 40)),
                (40, self.screen.get_display().get_size()[1] - 70))
            # On affiche le pokémon adverse
            self.screen.get_display().blit(
                pygame.transform.scale(pygame.image.load(self.info_espece["Path"]+"\\face.png"), (120, 120)).convert_alpha(),
                (self.screen.get_display().get_size()[0] - 120, 40))
            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render("You", False, (0, 0, 0)),
                                           (40, self.screen.get_display().get_size()[1] - 120))
            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(self.info_espece["Nom"], False, (0, 0, 0)),
                                           (self.screen.get_display().get_size()[0] - 200, 10))
            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(str(self.pv)+" /"+str(self.info_espece["PV"]), False, (0, 0, 0)),
                                           (self.screen.get_display().get_size()[0] - 200, 80))
            self.screen.get_display().blit(
                pygame.font.SysFont('Comic Sans MS', 30).render("Placeholder attack 1 : 5 dmg", False, (0, 0, 0)),
                (10, self.screen.get_display().get_size()[1]/2))

            if (pygame.K_a in self.pressed.keys() and self.pressed[pygame.K_a] is True) or self.pv <= 0:
                self.pressed[pygame.K_a] = False
                self.winner = 1

            if pygame.K_1 in self.pressed.keys() and self.pressed[pygame.K_1] is True:
                self.pressed[pygame.K_1] = False
                self.pv -= 5

        self.pressed = {}
        self.map.switch_map(self.origin)
        self.player.pos = Vector(self.player.pos.get()[0], self.player.pos.get()[1])
        self.cooldown = 120
        return None
