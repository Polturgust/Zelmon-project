import pygame
from vector import Vector
from dialogue import Dialogue


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

    def get_info_pokemons(self):
        self.equipe_joueur = self.game.save_selected.get_pokemon_equipe(0)
        self.info_pokemon_joueur = {"Info_pokemon": self.game.save_selected.get_info_pokemon(self.equipe_joueur)}
        self.info_pokemon_joueur["Info_espece"] = self.game.save_selected.get_info_espece(
            self.info_pokemon_joueur["Info_pokemon"]["ID_espece"])
        self.info_pokemon_joueur["Attaques"] = self.game.save_selected.get_attaques(
            self.info_pokemon_joueur["Info_pokemon"]["ID"])
        for i in self.info_pokemon_joueur["Attaques"]:
            i["PP_restants"] = self.game.save_selected.get_pp_restants(self.info_pokemon_joueur["Info_pokemon"]["ID"],i["ID"])

        self.info_espece_adv["Info_espece"] = self.game.save_selected.get_info_espece(self.id_poke_adv)
        if self.info_espece_adv["Info_espece"]["Type2"] is not None:
            self.info_espece_adv["Attaques"]=self.game.save_selected.get_attaques_par_type(self.info_espece_adv["Info_espece"]["Type1"],self.info_espece_adv["Info_espece"]["Type2"])

        else:
            self.info_espece_adv["Attaques"]=self.game.save_selected.get_attaques_par_type(self.info_espece_adv["Info_espece"]["Type1"])
        print(self.info_espece_adv["Attaques"])




    def combat_sauvage(self, id_poke_adv):
        """
        Fonction qui lance un combat.
        Un combat prend fin quand un des deux Pokémon est K.O ou si le joueur fuit en appuyant sur "a"
        """
        self.id_poke_adv=id_poke_adv
        self.info_espece_adv={}
        self.get_info_pokemons()
        self.winner = 0
        self.pv_adv = self.info_espece_adv["Info_espece"]["PV"]
        self.pv_joueur=self.info_pokemon_joueur["Info_pokemon"]["PV"]

        while self.winner == 0 and self.running:
            self.screen.update()
            self.map.update()
            self.pokemon_font = pygame.font.Font("assets\\font\\pokemon-ds-font.ttf", 65)

            self.bg_normal = pygame.image.load('assets\\images\\background_combat\\normal.png')
            self.bg_normal = pygame.transform.scale(self.bg_normal, (640,359))

            self.bg_park = pygame.image.load('assets\\images\\background_combat\\park.png')
            self.bg_park = pygame.transform.scale(self.bg_park, (640,359))

            self.bg_images = pygame.image.load('assets\\images\\background_combat\\neige.png')
            self.bg_images = pygame.transform.scale(self.bg_images, (640,359))

            self.bg_grotte = pygame.image.load('assets\\images\\background_combat\\grotte.png')
            self.bg_grotte = pygame.transform.scale(self.bg_grotte, (640,359))

            self.bg_roche = pygame.image.load('assets\\images\\background_combat\\roche.png')
            self.bg_roche = pygame.transform.scale(self.bg_roche, (640,359))

            self.bg_jungle = pygame.image.load('assets\\images\\background_combat\\jungle.png')
            self.bg_jungle = pygame.transform.scale(self.bg_jungle, (640,359))

            self.bg_eau = pygame.image.load('assets\\images\\background_combat\\eau.png')
            self.bg_eau = pygame.transform.scale(self.bg_eau, (640,359))

            self.hp_bars = pygame.image.load('assets\\images\\background_combat\\hp_bars.png')
            self.hp_bars = pygame.transform.scale(self.hp_bars, (640,359))

            self.screen.get_display().blit(self.bg_normal, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # On ferme le jeu si l'utilisateur ferme la fenêtre
                    self.running = False
                    return False
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée, on l'ajoute au dictionnaire des touches pressées
                    self.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False  # Si une touche est relâchée, on l'enlève du dictionnaire des touches pressées

            # On affiche le pokémon du joueur
            self.screen.get_display().blit(pygame.transform.scale(pygame.image.load(self.info_pokemon_joueur["Info_espece"]["Path"]+"\\dos.png"), (220, 220)),(50, 180))
            # On affiche le pokémon adverse
            self.screen.get_display().blit(pygame.transform.scale(pygame.image.load(self.info_espece_adv["Path"]+"\\face.png"), (220, 220)).convert_alpha(),(380, 62))
            #affiche les bars de PV
            self.screen.get_display().blit(self.hp_bars, (0,0))
            
            #affiche le nom du pokemon du joueur
            self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(self.info_pokemon_joueur["Info_pokemon"]["Nom"], False, (73, 73, 73)),(380, 250))
            #affiche les PV du pokemon du joueur
            self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(str(self.pv_joueur)+" / "+str(self.info_pokemon_joueur["Info_pokemon"]["PV"]), False, (73, 73, 73)), (80, 80))
            #affiche le niveau du pokemon du joueur
            self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(str(self.info_pokemon_joueur["Info_pokemon"]["Niveau"]), False, (73, 73, 73)), (590, 250))
            #affiche le nom du pokemon adverse
            self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(self.info_espece_adv["Nom"], False, (73, 73, 73)), (10, 48))
            #affiche les PV du pokemon adverse
            self.screen.get_display().blit(pygame.font.SysFont('pokemon_font', 30).render(str(self.pv_adv)+" /"+str(self.info_espece_adv["PV"]), False, (73, 73, 73)), (80, 80))
            #affiche le niveau du pokemon adverse
            self.screen.get_display().blit(pygame.transform.scale(pygame.image.load(self.info_espece_adv["Info_espece"]["Path"]+"\\face.png"), (220, 220)).convert_alpha(),(380, 62))
            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(self.info_pokemon_joueur["Info_pokemon"]["Nom"], False, (0, 0, 0)),(130, self.screen.get_display().get_size()[1] - 100))


            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(self.info_espece_adv["Info_espece"]["Nom"], False, (0, 0, 0)),
                                           (self.screen.get_display().get_size()[0] - 200, 10))
            self.screen.get_display().blit(pygame.font.SysFont('Comic Sans MS', 30).render(str(self.pv_adv)+" /"+str(self.info_espece_adv["Info_espece"]["PV"]), False, (0, 0, 0)),
                                           (self.screen.get_display().get_size()[0] - 200, 80))
            coord=self.screen.get_display().get_size()[1]/4
            nb=1
            for i in self.info_pokemon_joueur["Attaques"]:
                self.screen.get_display().blit(
                pygame.font.SysFont('pokemon_font', 30).render(str(nb)+" : "+str(i["Nom"])+" : "+str(i["Puissance"])+" dégâts", False, (73, 73, 73)),
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


    def attaquer(self,attaque_joueur,attaque_adv):
        self.attaque_joueur=attaque_joueur
        self.attaque_adv=attaque_adv
