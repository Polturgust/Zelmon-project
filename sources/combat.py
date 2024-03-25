import pygame
from random import *
from vector import Vector
from math import *
from dialogue import Dialogue


class Combat:
    def __init__(self, game, screen, player, map, origin, save):
        self.game = game
        self.screen = screen
        self.player = player
        self.running = True
        self.map = map
        self.pressed = {}
        self.origin = origin
        self.save = save

    def get_info_pokemons(self,update_pv=False):
        """
        Récupère les informations sur les pokémons en combat

        Préconditions :
            - update_pv doit être un booléen

        Renvoie :
            - Rien, les informations sont directement mises à jour dans les dictionnaires


        """
        if not update_pv:
            pv=self.info_espece_adv["Info_pokemon"]["PV"]
        self.equipe_joueur = self.game.save_selected.get_pokemon_equipe(0)
        self.info_pokemon_joueur = {"Info_pokemon": self.game.save_selected.get_info_pokemon(self.equipe_joueur)}
        self.info_pokemon_joueur["Info_espece"] = self.game.save_selected.get_info_espece(
            self.info_pokemon_joueur["Info_pokemon"]["ID_espece"])
        self.info_pokemon_joueur["Attaques"] = self.game.save_selected.get_attaques(
            self.info_pokemon_joueur["Info_pokemon"]["ID"])
        for i in self.info_pokemon_joueur["Attaques"]:
            i["PP_restants"] = self.game.save_selected.get_pp_restants(self.info_pokemon_joueur["Info_pokemon"]["ID"],
                                                                       i["ID"])

        self.info_espece_adv["Info_espece"] = self.game.save_selected.get_info_espece(self.id_poke_adv)
        if self.info_espece_adv["Info_espece"]["Type2"] is not None:
            self.info_espece_adv["Attaques"] = self.game.save_selected.get_attaques_par_type(
                self.info_espece_adv["Info_espece"]["Type1"], self.info_espece_adv["Info_espece"]["Type2"])

        else:
            self.info_espece_adv["Attaques"] = self.game.save_selected.get_attaques_par_type(
                self.info_espece_adv["Info_espece"]["Type1"])

        self.info_espece_adv["Info_pokemon"] = {}
        self.info_espece_adv["Info_pokemon"]["Vitesse"] = randint(0, 100)
        if update_pv:
            self.info_espece_adv["Info_pokemon"]["PV"] = self.info_espece_adv["Info_espece"]["PV"]
        else:
            self.info_espece_adv["Info_pokemon"]["PV"]=pv

    def combat_sauvage(self, id_poke_adv):
        """
        Fonction qui lance un combat.
        Un combat prend fin quand un des deux Pokémon est K.O ou si le joueur fuit en appuyant sur "a"
        """
        self.id_poke_adv = id_poke_adv
        self.info_espece_adv = {}
        self.get_info_pokemons(True)
        self.winner = None

        while self.winner is None and self.running:
            self.screen.update()
            self.map.update()
            self.afficher()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # On ferme le jeu si l'utilisateur ferme la fenêtre
                    self.running = False
                    return False
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée, on l'ajoute au dictionnaire des touches pressées
                    self.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed[
                        event.key] = False  # Si une touche est relâchée, on l'enlève du dictionnaire des touches pressées

            # On affiche le pokémon du joueur
            self.screen.get_display().blit(
                pygame.transform.scale(pygame.image.load(self.info_pokemon_joueur["Info_espece"]["Path"] + "\\dos.png"),
                                       (220, 220)), (50, 180))
            # On affiche le pokémon adverse
            self.screen.get_display().blit(
                pygame.transform.scale(pygame.image.load(self.info_espece_adv["Info_espece"]["Path"] + "\\face.png"),
                                       (220, 220)).convert_alpha(), (380, 62))
            # affiche les barres d'info
            self.screen.get_display().blit(self.barre_info, (0, 0))

            # affiche le nom du pokemon du joueur
            self.screen.get_display().blit(
                pygame.font.SysFont('pokemon_font', 30).render(self.info_pokemon_joueur["Info_pokemon"]["Nom"], False,
                                                               (73, 73, 73)), (380, 250))
            # affiche les PV du pokemon du joueur
            self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(
                str(self.info_pokemon_joueur["Info_pokemon"]["PV"]) + " / " + str(
                    self.info_pokemon_joueur["Info_espece"]["PV"]), False, (73, 73, 73)), (80, 100))
            # affiche le niveau du pokemon du joueur
            self.screen.get_display().blit(
                pygame.font.SysFont('pokemon_font', 30).render(str(self.info_pokemon_joueur["Info_pokemon"]["Niveau"]),
                                                               False, (73, 73, 73)), (590, 250))
            # affiche le nom du pokemon adverse
            self.screen.get_display().blit(
                pygame.font.SysFont('pokemon_font', 30).render(self.info_espece_adv["Info_espece"]["Nom"], False,
                                                               (73, 73, 73)), (10, 48))
            # affiche les PV du pokemon adverse
            self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(
                str(self.info_espece_adv["Info_pokemon"]["PV"]) + " /" + str(self.info_espece_adv["Info_espece"]["PV"]),
                False, (73, 73, 73)), (80, 80))
            # affiche le niveau du pokemon adverse
            self.screen.get_display().blit(
                pygame.transform.scale(pygame.image.load(self.info_espece_adv["Info_espece"]["Path"] + "\\face.png"),
                                       (220, 220)).convert_alpha(), (380, 62))
            self.screen.get_display().blit(
                pygame.font.SysFont('Comic Sans MS', 30).render(self.info_pokemon_joueur["Info_pokemon"]["Nom"], False,
                                                                (0, 0, 0)),
                (130, self.screen.get_display().get_size()[1] - 100))
            # affiche le niveau du pokemon adverse

            # gere la taille de la barre de pv
            self.taille_conteneur_barre_pv_x = 120
            self.ratio_barre_pv = self.taille_conteneur_barre_pv_x / self.info_espece_adv["Info_espece"]["PV"]
            self.taille_voulue_x = self.info_pokemon_joueur["Info_pokemon"]["PV"] * self.ratio_barre_pv

            # essaye d'afficher une barre de pv
            self.rect_bare_pv = pygame.Rect(600, 300, self.ratio_barre_pv, 7)
            self.rect_bare_pv.inflate_ip(50, 1)
            self.green_hp_bar = pygame.draw.rect(self.screen.get_display(), (0, 255, 0), self.rect_bare_pv)

            self.screen.get_display().blit(
                pygame.font.SysFont('Comic Sans MS', 30).render(self.info_espece_adv["Info_espece"]["Nom"], False,
                                                                (0, 0, 0)),
                (self.screen.get_display().get_size()[0] - 200, 10))
            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(
                str(self.info_espece_adv["Info_pokemon"]["PV"]) + " /" + str(self.info_espece_adv["Info_espece"]["PV"]),
                False, (0, 0, 0)),
                                           (self.screen.get_display().get_size()[0] - 200, 80))
            coord = self.screen.get_display().get_size()[1] / 4
            nb = 1
            for i in self.info_pokemon_joueur["Attaques"]:
                self.screen.get_display().blit(
                    pygame.font.SysFont('pokemon_font', 30).render(
                        str(nb) + " : " + str(i["Nom"]) + " : " + str(i["Puissance"]) + " dégâts", False, (73, 73, 73)),
                    (10, coord))
                coord += 40
                nb += 1

            if (pygame.K_a in self.pressed.keys() and self.pressed[pygame.K_a] is True) or self.info_espece_adv["Info_espece"]["PV"] <= 0:
                self.pressed[pygame.K_a] = False
                self.winner = True

            if pygame.K_1 in self.pressed.keys() and self.pressed[pygame.K_1] is True:
                self.pressed[pygame.K_1] = False
                self.attaquer(self.info_pokemon_joueur["Attaques"][0], self.info_espece_adv["Attaques"][randint(0, 3)])

            if pygame.K_2 in self.pressed.keys() and self.pressed[pygame.K_2] is True and len(
                    self.info_pokemon_joueur["Attaques"]) >= 2:
                self.pressed[pygame.K_2] = False
                self.attaquer(self.info_pokemon_joueur["Attaques"][1], self.info_espece_adv["Attaques"][randint(0, 3)])

            if pygame.K_3 in self.pressed.keys() and self.pressed[pygame.K_3] is True and len(
                    self.info_pokemon_joueur["Attaques"]) >= 3:
                self.pressed[pygame.K_3] = False
                self.attaquer(self.info_pokemon_joueur["Attaques"][2], self.info_espece_adv["Attaques"][randint(0, 3)])

            if pygame.K_4 in self.pressed.keys() and self.pressed[pygame.K_4] is True and len(
                    self.info_pokemon_joueur["Attaques"]) >= 4:
                self.pressed[pygame.K_4] = False
                self.attaquer(self.info_pokemon_joueur["Attaques"][3], self.info_espece_adv["Attaques"][randint(0, 3)])

            if pygame.K_5 in self.pressed.keys() and self.pressed[pygame.K_5] is True:
                self.pressed[pygame.K_5]=False
                if self.tenter_capture():
                    self.winner=True

        self.pressed = {}
        self.map.switch_map(self.origin)
        self.player.pos = Vector(self.player.pos.get()[0], self.player.pos.get()[1])
        self.cooldown = 120
        self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur, self.info_pokemon_joueur["Attaques"])
        return self.winner

    def attaquer(self, attaque_joueur, attaque_adv, att="J"):
        self.attaque_joueur = attaque_joueur
        self.attaque_adv = attaque_adv
        if att == "J":
            self.nom_att = self.info_pokemon_joueur["Info_pokemon"]["Nom"]
            self.nom_def = self.info_espece_adv["Info_espece"]["Nom"]
        else:
            self.nom_def = self.info_pokemon_joueur["Info_pokemon"]["Nom"]
            self.nom_att = self.info_espece_adv["Info_espece"]["Nom"]

        if self.info_espece_adv["Info_espece"]["Vitesse"] > self.info_pokemon_joueur["Info_espece"]["Vitesse"]:
            reussi = randint(0, 100) <= self.attaque_adv["Precision"]
            Dialogue(self.nom_att + " utilise " + self.attaque_joueur['Nom'] + " !", self.screen, self.map,
                     self).afficher(True)
            if reussi:
                self.info_pokemon_joueur["Info_pokemon"]["PV"] -= self.get_puissance_attaque(self.attaque_adv, "S")
                print("Pokemon advrese attaque en premier")
                print(self.info_pokemon_joueur["Info_pokemon"]["PV"])
                if self.info_pokemon_joueur["Info_pokemon"]["PV"] <= 0 and not self.game.save_selected.a_pokemons_vivants(0)[0]:
                    self.info_pokemon_joueur["Info_pokemon"]["PV"] = 0
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur, None)
                    self.winner = False
                elif self.info_pokemon_joueur["Info_pokemon"]["PV"] <=0:
                    print("pokémon du joueur tué :(")
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur,None)
                    if  self.game.save_selected.a_pokemons_vivants(0)[0] :
                        self.game.save_selected.equiper_pokemon(0, self.game.save_selected.a_pokemons_vivants(0)[1][0])
                        self.get_info_pokemons()


            else:
                Dialogue("L'attaque a échoué...", self.screen, self.map, self).afficher(True)

            reussi = randint(0, 100) <= self.attaque_joueur["Precision"]
            Dialogue(self.nom_def + " utilise " + self.attaque_adv['Nom'] + " !", self.screen, self.map, self).afficher(
                True)
            if reussi:
                self.info_espece_adv["Info_pokemon"]["PV"] -= self.get_puissance_attaque(self.attaque_joueur, "S")
                if self.info_espece_adv["Info_pokemon"]["PV"] <= 0:
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur, None)
                    self.info_espece_adv["Info_pokemon"]["PV"] = 0
                    self.winner = True

            else:
                Dialogue("L'attaque a échoué...", self.screen, self.map, self).afficher(True)



        else:
            reussi = randint(0, 100) <= self.attaque_joueur["Precision"]
            Dialogue(self.nom_def + " utilise " + self.attaque_adv['Nom'] + " !", self.screen, self.map,
                     self).afficher(True)
            if reussi:
                self.info_espece_adv["Info_pokemon"]["PV"] -= self.get_puissance_attaque(self.attaque_joueur, "S")
                if self.info_espece_adv["Info_pokemon"]["PV"] <= 0:
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur, None)
                    self.info_espece_adv["Info_pokemon"]["PV"] = 0
                    self.winner = True

            else:
                Dialogue("L'attaque a échoué...", self.screen, self.map, self).afficher(True)

            reussi = randint(0, 100) <= self.attaque_adv["Precision"]
            Dialogue(self.nom_att + " utilise " + self.attaque_joueur['Nom'] + " !", self.screen, self.map,
                     self).afficher(True)
            if reussi:
                self.info_pokemon_joueur["Info_pokemon"]["PV"] -= self.get_puissance_attaque(self.attaque_adv, "S")
                print("Pokemon advrese attaque en 2e")
                if self.info_pokemon_joueur["Info_pokemon"]["PV"] <= 0 and not self.game.save_selected.a_pokemons_vivants(0)[0]:
                    self.info_pokemon_joueur["Info_pokemon"]["PV"] = 0
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur, None)
                    self.winner = False
                elif self.info_pokemon_joueur["Info_pokemon"]["PV"] <= 0:
                    print("pokémon joueur tué :(")
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur,None)
                    if self.game.save_selected.a_pokemons_vivants(0)[0]:
                        self.game.save_selected.equiper_pokemon(0, self.game.save_selected.a_pokemons_vivants(0)[1][0])
                        self.get_info_pokemons()

            else:
                print("L'attaque a échoué...")

    def get_puissance_attaque(self, attaque, attaquant="J"):
        if attaquant == "J":
            self.data_att = self.info_pokemon_joueur
            self.data_def = self.info_espece_adv


        elif attaquant == "S":
            self.data_att = self.info_espece_adv
            self.data_att["Info_pokemon"]["Niveau"] = 3
            self.data_def = self.info_pokemon_joueur

        calcul = floor((self.data_att["Info_pokemon"]["Niveau"] * 0.4) + 1)
        calcul = calcul * attaque["Puissance"] * self.data_att["Info_espece"]["Attaque"]
        calcul = floor(calcul / self.data_def["Info_espece"]["Defense"])
        calcul = floor(calcul / 50) + 2
        coeff = uniform(0.85, 1)
        if attaque["Type"] in (
                self.data_att["Info_espece"]["Type1"], self.data_att["Info_espece"]["Type2"]):
            coeff = coeff * 1.5
        coeff = coeff * self.game.save_selected.get_avantages(attaque["Type"], self.data_def["Info_espece"]["Type1"])
        if self.data_def["Info_espece"]["Type2"] is not None:
            coeff = coeff * self.game.save_selected.get_avantages(attaque["Type"],
                                                                  self.data_def["Info_espece"]["Type2"])

        return round(calcul * coeff)

    def afficher(self):
        """
        Fonction permettant d'afficher le combat et les différentes informations
        """
        self.pokemon_font = pygame.font.Font("assets\\font\\pokemon-ds-font.ttf", 65)

        self.bg_normal = pygame.image.load('assets\\images\\background_combat\\normal.png')
        self.bg_normal = pygame.transform.scale(self.bg_normal, (640, 359))

        self.bg_park = pygame.image.load('assets\\images\\background_combat\\park.png')
        self.bg_park = pygame.transform.scale(self.bg_park, (640, 359))

        self.bg_images = pygame.image.load('assets\\images\\background_combat\\neige.png')
        self.bg_images = pygame.transform.scale(self.bg_images, (640, 359))

        self.bg_grotte = pygame.image.load('assets\\images\\background_combat\\grotte.png')
        self.bg_grotte = pygame.transform.scale(self.bg_grotte, (640, 359))

        self.bg_roche = pygame.image.load('assets\\images\\background_combat\\roche.png')
        self.bg_roche = pygame.transform.scale(self.bg_roche, (640, 359))

        self.bg_jungle = pygame.image.load('assets\\images\\background_combat\\jungle.png')
        self.bg_jungle = pygame.transform.scale(self.bg_jungle, (640, 359))

        self.bg_eau = pygame.image.load('assets\\images\\background_combat\\eau.png')
        self.bg_eau = pygame.transform.scale(self.bg_eau, (640, 359))

        self.barre_info = pygame.image.load('assets\\images\\background_combat\\hp_bars.png')
        self.barre_info = pygame.transform.scale(self.barre_info, (640, 359))

        self.screen.get_display().blit(self.bg_normal, (0, 0))
        # On affiche le pokémon du joueur
        self.screen.get_display().blit(
            pygame.transform.scale(pygame.image.load(self.info_pokemon_joueur["Info_espece"]["Path"] + "\\dos.png"),
                                   (220, 220)), (50, 180))
        # On affiche le pokémon adverse
        self.screen.get_display().blit(
            pygame.transform.scale(pygame.image.load(self.info_espece_adv["Info_espece"]["Path"] + "\\face.png"),
                                   (220, 220)).convert_alpha(), (380, 62))
        # affiche les barres d'info
        self.screen.get_display().blit(self.barre_info, (0, 0))

        # affiche le nom du pokemon du joueur
        self.screen.get_display().blit(
            pygame.font.SysFont('pokemon_font', 30).render(self.info_pokemon_joueur["Info_pokemon"]["Nom"], False,
                                                           (73, 73, 73)), (380, 250))
        # affiche les PV du pokemon du joueur
        self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(
            str(self.info_pokemon_joueur["Info_pokemon"]["PV"]) + " /" + str(self.info_pokemon_joueur["Info_espece"]["PV"]),
            False, (0, 0, 0)), (400, 270))
        # affiche le niveau du pokemon du joueur
        self.screen.get_display().blit(
            pygame.font.SysFont('pokemon_font', 30).render(str(self.info_pokemon_joueur["Info_pokemon"]["Niveau"]),
                                                           False, (73, 73, 73)), (590, 250))
        # affiche le nom du pokemon adverse
        self.screen.get_display().blit(
            pygame.font.SysFont('pokemon_font', 30).render(self.info_espece_adv["Info_espece"]["Nom"], False,
                                                           (73, 73, 73)), (10, 48))
        # affiche les PV du pokemon adverse
        self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(
            str(self.info_espece_adv["Info_pokemon"]["PV"]) + " /" + str(self.info_espece_adv["Info_espece"]["PV"]),
            False, (73, 73, 73)), (80, 80))
        # affiche le niveau du pokemon adverse
        self.screen.get_display().blit(
            pygame.transform.scale(pygame.image.load(self.info_espece_adv["Info_espece"]["Path"] + "\\face.png"),
                                   (220, 220)).convert_alpha(), (380, 62))
        self.screen.get_display().blit(
            pygame.font.SysFont('Comic Sans MS', 30).render(self.info_pokemon_joueur["Info_pokemon"]["Nom"], False,
                                                            (0, 0, 0)),
            (130, self.screen.get_display().get_size()[1] - 100))
        # affiche le niveau du pokemon adverse

        # gere la taille de la barre de pv
        self.taille_conteneur_barre_pv_x = 600
        self.ratio_barre_pv = self.taille_conteneur_barre_pv_x / self.info_espece_adv["Info_espece"]["PV"]
        self.taille_voulue_x = self.info_pokemon_joueur["Info_pokemon"]["PV"] * self.ratio_barre_pv

        # essaye d'afficher une barre de pv
        self.rect_bare_pv = pygame.Rect(600, 300, self.ratio_barre_pv, 7)
        self.rect_bare_pv.inflate_ip(50, 1)
        self.green_hp_bar = pygame.draw.rect(self.screen.get_display(), (0, 255, 0), self.rect_bare_pv)

        self.screen.get_display().blit(
            pygame.font.SysFont('Comic Sans MS', 30).render(self.info_espece_adv["Info_espece"]["Nom"], False,
                                                            (0, 0, 0)),
            (self.screen.get_display().get_size()[0] - 200, 10))
        self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(
            str(self.info_espece_adv["Info_pokemon"]["PV"]) + " /" + str(self.info_espece_adv["Info_espece"]["PV"]),
            False, (0, 0, 0)), (self.screen.get_display().get_size()[0] - 200, 80))


    def tenter_capture(self):
        """
        Fonction calculant si le pokémon est capturé lorsqu'on essaie de le capturer, et l'ajoute à la base de données si on réussit à la capturer
        Sinon, on renvoie False.
        """

        self.chance_capture=randint(0,self.info_espece_adv["Info_espece"]["PV"]-self.info_espece_adv["Info_pokemon"]["PV"])
        if self.chance_capture<5:
            Dialogue("Vous capturez le pokémon !",self.screen,self.map,self).afficher()
            nom=input("Quel nom voulez-vous donner à votre Pokémon ? Laisser vide pour lui laisser le nom de l'espèce : ")
            if nom=="":
                nom=self.info_espece_adv["Info_espece"]["Nom"]
            if len(self.game.save_selected.get_equipe(0))<6:
                id=self.game.save_selected.capturer_pokemon({"ID":self.info_espece_adv["Info_espece"]["ID_espece"],"Nom":nom,"Niveau":randint(0,10),"XP":0,"PV":self.info_espece_adv["Info_pokemon"]["PV"],"Statut":"None"},0,self.info_espece_adv["Attaques"])
                self.game.save_selected.deplacer_PC_vers_equipe(id,0)
                self.game.save_selected.equiper_pokemon(0,id)
            else:
                self.game.save_selected.capturer_pokemon(
                    {"ID": self.info_espece_adv["Info_espece"]["ID_espece"], "Nom": nom, "Niveau": randint(0, 10),
                     "XP": 0, "PV": self.info_espece_adv["Info_pokemon"]["PV"], "Statut": "None"},0, self.info_espece_adv["Attaques"])
            return True
        else:
            return False
