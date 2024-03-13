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
        self.equipe_joueur=self.game.save_selected.get_pokemon_equipe(0)
        self.info_pokemon_joueur={"Info_pokemon":self.game.save_selected.get_info_pokemon(self.equipe_joueur)}
        self.info_pokemon_joueur["Info_espece"]=self.game.save_selected.get_info_espece(self.info_pokemon_joueur["Info_pokemon"]["ID_espece"])
        self.info_pokemon_joueur["Attaques"]=self.game.save_selected.get_attaques(self.info_pokemon_joueur["Info_pokemon"]["ID"])

        print(self.info_pokemon_joueur)

        self.info_espece_adv=self.game.save_selected.get_info_espece(id_poke_adv)
        print(self.info_espece_adv["Nom"] + " veut se battre !")

        self.winner = 0
        self.pv_adv = self.info_espece_adv["PV"]
        self.pv_joueur=self.info_pokemon_joueur["Info_pokemon"]["PV"]

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
                pygame.transform.scale(pygame.image.load(self.info_pokemon_joueur["Info_espece"]["Path"]+"\\dos.png"), (120, 120)),
                (10, self.screen.get_display().get_size()[1] - 130))
            # On affiche le pokémon adverse
            self.screen.get_display().blit(
                pygame.transform.scale(pygame.image.load(self.info_espece_adv["Path"]+"\\face.png"), (120, 120)).convert_alpha(),
                (self.screen.get_display().get_size()[0] - 120, 40))
            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(self.info_pokemon_joueur["Info_pokemon"]["Nom"], False, (0, 0, 0)),
                                           (130, self.screen.get_display().get_size()[1] - 100))

            self.screen.get_display().blit(
                pygame.font.SysFont('Comic Sans MS', 30).render(str(self.pv_joueur)+" / "+str(self.info_pokemon_joueur["Info_pokemon"]["PV"]), False,
                                                                (0, 0, 0)),
                (130, self.screen.get_display().get_size()[1] - 50))

            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(self.info_espece_adv["Nom"], False, (0, 0, 0)),
                                           (self.screen.get_display().get_size()[0] - 200, 10))
            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(str(self.pv_adv)+" /"+str(self.info_espece_adv["PV"]), False, (0, 0, 0)),
                                           (self.screen.get_display().get_size()[0] - 200, 80))
            coord=self.screen.get_display().get_size()[1]/4
            nb=1
            for i in self.info_pokemon_joueur["Attaques"]:
                self.screen.get_display().blit(
                pygame.font.SysFont('Comic Sans MS', 30).render(str(nb)+" : "+str(i["Nom"])+" : "+str(i["Puissance"])+" dégâts", False, (0, 0, 0)),
                (10, coord))
                coord+=40
                nb+=1

            if (pygame.K_a in self.pressed.keys() and self.pressed[pygame.K_a] is True) or self.pv_adv <= 0:
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
