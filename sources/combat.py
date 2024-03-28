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

    def get_info_pokemons(self, update_pv=False):
        """
        Récupère les informations sur les pokémons en combat

        Préconditions :
            - update_pv doit être un booléen

        Renvoie :
            - Rien, les informations sont directement mises à jour dans les dictionnaires


        """
        if update_pv:
            pv = self.info_espece_adv["Info_pokemon"]["PV"]

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
        self.info_espece_adv["Info_pokemon"]["PV"] = self.info_espece_adv["Info_espece"]["PV"]
        self.info_espece_adv["Info_pokemon"]["Niveau"]=str(randint(1,self.info_pokemon_joueur["Info_pokemon"]["Niveau"]))
        if update_pv:
            self.info_espece_adv["Info_pokemon"]["PV"]=pv

    def combat_sauvage(self, id_poke_adv):
        """
        Lance et gère un combat entre le joueur et un pokémon sauvage dont l'ID est donné en argument.

        Précondition :
            - id_poke_adv doit être un entier naturel correspondant à l'id d'un pokemon

        Renvoie :
            - True si le combat est gagné par le joueur
            - False si le joueur perd
        """
        self.id_poke_adv = id_poke_adv
        self.info_espece_adv = {}
        self.get_info_pokemons()
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
                self.tenter_capture()

        self.pressed = {}
        self.map.switch_map(self.origin)
        self.player.pos = Vector(self.player.pos.get()[0], self.player.pos.get()[1])
        self.cooldown = 120
        self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur)
        return self.winner

    def attaquer(self, attaque_joueur, attaque_adv):
        """
        Lance un échange d'attaques une fois que le joueur a choisi une attaque : gère la priorité des attaques et la probabilité de réussite

        Préconditions :
            - attaque_joueur et attaque_adv doivent être des dictionnaires contenant les informations sur les capacités des attaques du joueur et du pokémon adverse

        Renvoie :
            - rien, les dégâts sont automatiquement appliqués dans les statistiques des pokémons.
        """
        self.attaque_joueur = attaque_joueur
        self.attaque_adv = attaque_adv
        self.nom_att = self.info_pokemon_joueur["Info_pokemon"]["Nom"]
        self.nom_def = self.info_espece_adv["Info_espece"]["Nom"]

        if self.info_espece_adv["Info_espece"]["Vitesse"] > self.info_pokemon_joueur["Info_espece"]["Vitesse"]:
            reussi = randint(0, 100) <= self.attaque_adv["Precision"]
            Dialogue(self.nom_att + " utilise " + self.attaque_joueur['Nom'] + " !", self.screen, self.map,
                     self).afficher(True)
            if reussi:
                self.info_pokemon_joueur["Info_pokemon"]["PV"] -= self.get_puissance_attaque(self.attaque_adv, "S")
                if self.info_pokemon_joueur["Info_pokemon"]["PV"] <= 0 and not self.game.save_selected.a_pokemons_vivants(0)[0]:
                    self.info_pokemon_joueur["Info_pokemon"]["PV"] = 0
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur)
                    self.winner = False
                elif self.info_pokemon_joueur["Info_pokemon"]["PV"] <=0:
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur)
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
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur)
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
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur)
                    self.info_espece_adv["Info_pokemon"]["PV"] = 0
                    self.winner = True

            else:
                Dialogue("L'attaque a échoué...", self.screen, self.map, self).afficher(True)

            reussi = randint(0, 100) <= self.attaque_adv["Precision"]
            Dialogue(self.nom_att + " utilise " + self.attaque_joueur['Nom'] + " !", self.screen, self.map,
                     self).afficher(True)
            if reussi:
                self.info_pokemon_joueur["Info_pokemon"]["PV"] -= self.get_puissance_attaque(self.attaque_adv, "S")
                if self.info_pokemon_joueur["Info_pokemon"]["PV"] <= 0 and not self.game.save_selected.a_pokemons_vivants(0)[0]:
                    self.info_pokemon_joueur["Info_pokemon"]["PV"] = 0
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur)
                    self.winner = False
                elif self.info_pokemon_joueur["Info_pokemon"]["PV"] <= 0:
                    self.game.save_selected.sauvegarder_info_pokemon(self.info_pokemon_joueur)
                    if self.game.save_selected.a_pokemons_vivants(0)[0]:
                        self.game.save_selected.equiper_pokemon(0, self.game.save_selected.a_pokemons_vivants(0)[1][0])
                        self.get_info_pokemons()

            else:
                Dialogue("L'attaque a échoué...", self.screen, self.map, self).afficher(True)

    def get_puissance_attaque(self, attaque, attaquant="J"):
        """
        Renvoie la puissance d'une attaque (calcul officiel prenant en compte, entre autres, le niveau du pokémon, le type de l'attaque, et les statistiques d'attaque et de défense des deux pokémons.

        Valeurs en entrée :
            - attaque : dictionnaire contenant les informations sur l'attaque dont on souhaite calculer la puissance
            - attaquant : chaîne de caractère indiquant si l'attaquant est le joueur ou le pokémon sauvage

        - Préconditions :
            - attaque doit être un dictionnaire contenant les informations sur l'attaque du pokémon.
            - attaquant doit être une chaîne de caractères égale à "J" ou "S"

        Renvoie :
            - Un entier naturel correspondant au nombre de points de dégâts infligés à l'adversaire
        """
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
        Affiche et met à jour l'affichage des informations et des images des pokémons durant le combat.

        Ne prend aucun argument.

        Ne renvoie rien.
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
        self.texture_pokemon_joueur=pygame.transform.scale(pygame.image.load(self.info_pokemon_joueur["Info_espece"]["Path"] + "\\dos.png"),(220, 220))
        self.screen.get_display().blit(self.texture_pokemon_joueur
            , (50, self.texture_pokemon_joueur.get_height()-81))
        
        # On affiche le pokémon adverse
        self.texture_pokemon_adv=pygame.transform.scale(pygame.image.load(self.info_espece_adv["Info_espece"]["Path"] + "\\face.png"),
                                   (220, 220)).convert_alpha()
        self.screen.get_display().blit(self.texture_pokemon_adv, (380, self.texture_pokemon_adv.get_height()-165))
        
        # affiche les barres d'info
        self.screen.get_display().blit(self.barre_info, (0, 0))

        # affiche le nom du pokemon du joueur
        self.screen.get_display().blit(
            pygame.font.SysFont('pokemon_font', 30).render(self.info_pokemon_joueur["Info_pokemon"]["Nom"], False,
                                                           (73, 73, 73)), (380, 251))
        # affiche les PV du pokemon du joueur
        self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(
            str(self.info_pokemon_joueur["Info_pokemon"]["PV"]) + "    " + str(
                self.info_pokemon_joueur["Info_espece"]["PV"]), False, (73, 73, 73)), (515, 300))

        # affiche le niveau du pokemon du joueur
        self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(str(self.info_pokemon_joueur["Info_pokemon"]["Niveau"]), False, (73, 73, 73)), (590, 251))

        # affiche le nom du pokemon adverse
        self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(self.info_espece_adv["Info_espece"]["Nom"], False, (73, 73, 73)), (10, 50))

        # Affiche le niveau du pokémon adverse
        self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(str(self.info_espece_adv["Info_pokemon"]["Niveau"]), False, (73, 73, 73)), (225, 50))

        # Barre de pv du Pokémon adverse
        taille_barre_adv = (self.info_espece_adv["Info_pokemon"]["PV"] / self.info_espece_adv["Info_espece"]["PV"] * 100) * 120 / 100
        barre_adv_rect = pygame.Rect(126, 83, taille_barre_adv, 8)
        pygame.draw.rect(self.screen.get_display(), (0, 255, 0), barre_adv_rect)

        # gere la taille de la barre de pv du Pokémon du joueur
        self.taille_voulue_x = (self.info_pokemon_joueur["Info_pokemon"]["PV"] /
                                self.info_pokemon_joueur["Info_espece"]["PV"] * 100) * 120 / 100

        # on affiche la barre de pv du Pokémon du joueur
        self.rect_barre_pv = pygame.Rect(500, 284, self.taille_voulue_x, 8)
        pygame.draw.rect(self.screen.get_display(), (0, 255, 0), self.rect_barre_pv)

        coords = [(10,390),(10,440),(320,390),(320,440)]
        nb=1
        for i in self.info_pokemon_joueur["Attaques"]:
            self.screen.get_display().blit(
                pygame.font.SysFont('pokemon_font', 30).render(
                    str(nb) + " : " + str(i["Nom"]) + ", " + str(i["Puissance"]), False, (73, 73, 73)),
                (coords[nb-1][0], coords[nb-1][1]))
            nb += 1


    def tenter_capture(self):
        """
        Choisit lors de l'appui sur la touche 5 si le pokémon est capturé ou non.

        Ne prend aucun argument

        """
        self.chance_capture = randint(0, self.info_espece_adv["Info_espece"]["PV"]-(self.info_espece_adv["Info_espece"]["PV"]-self.info_espece_adv["Info_pokemon"]["PV"]))
        if self.chance_capture < 10:
            Dialogue("Vous capturez le pokémon !", self.screen, self.map, self).afficher()
            nom = input("Quel nom voulez-vous donner à votre Pokémon ? Laisser vide pour lui laisser le nom de l'espèce : ")
            if nom == "":
                nom = self.info_espece_adv["Info_espece"]["Nom"]
            self.game.save_selected.capturer_pokemon({"1":self.info_espece_adv["Info_espece"]["ID_espece"],"2":nom,"3":randint(0,10),"4":0,"5":self.info_espece_adv["Info_pokemon"]["PV"],"6":"None"},0)
            self.winner=True
        else:
            Dialogue("La capture a échoué...",self.screen,self.map,self).afficher()
            self.attaquer(self.game.save_selected.get_details_attaque(99),self.info_espece_adv["Attaques"][randint(0, 3)])
