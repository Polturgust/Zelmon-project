import pygame
from random import randint
from moviepy.editor import VideoFileClip
import os

from screen import Screen
from map import Map
from player import Player
from combat import Combat
from pnj import *
from SQL_requests import *
from dialogue import *
from audio import SoundManager


class Game:
    def __init__(self):
        # set the game to running
        self.running = True
        self.playing = False
        # initialise the screen
        self.screen = Screen()
        # create a player
        self.player = Player(self)
        # initialise the screen
        self.map = Map(self.screen, self.player)
        # initialise the sound manager
        self.sound_manager = SoundManager()

        # On crée un dictionnaire qui contient tous les pnjs sous la forme : {"Nom-pnj" : Instance_classe_pnj}
        self.pnjs = dict()

        # On initialise les variables pour le mouvement du joueur :
        # Son dernier mouvement (qui par défaut est un déplacement vers le bas)
        self.last_move = "S"
        # La liste des mouvements inverses, utile dans la gestion des collisions
        self.inverse = {"NW": "SE", "NE": "SW", "SW": "NE", "SE": "NW", "N": "S", "S": "N", "E": "W", "W": "E"}
        # on crée un dictionnaire qui contient les touches pressées (permet de rester appuyé sur une touche → utile pour se déplacer)
        self.pressed = dict()

        self.cooldown = 0

        self.save_selected = None  # Une sauvegarde est-elle sélectionnée ?

    def run(self):
        # Lance la vidéo d'introduction au lancement du jeu → appuyer sur Esc permet d'interrompre la vidéo
        VideoFileClip("assets/videos/Pokemon Heart Gold  Opening US_480p.mp4").resize((640, 480)).preview()

        # On vérifie si on a des sauvegardes, sinon on crée une sauvegarde nommée sauvegarde1
        nb_sauvegardes = len(os.listdir("databases")) - 1

        if nb_sauvegardes == 0:
            create_save(1)
            nb_sauvegardes += 1

        background = pygame.image.load("assets/images/zelda.webp")
        background = pygame.transform.scale(background, (640, 480))

        save_selection = pygame.image.load("assets/images/Sélecteur.png").convert_alpha()
        save_selection = pygame.transform.scale(save_selection, (450, 100))
        save1_btn = pygame.image.load("assets/images/Sauvegarde1_btn.png").convert_alpha()
        save1_btn = pygame.transform.scale(save1_btn, (400, 50))
        save2_btn = pygame.image.load("assets/images/Sauvagarde2_btn.png").convert_alpha()
        save2_btn = pygame.transform.scale(save2_btn, (400, 50))
        save3_btn = pygame.image.load("assets/images/Sauvegarde3_btn.png").convert_alpha()
        save3_btn = pygame.transform.scale(save3_btn, (400, 50))
        new_save_btn = pygame.image.load("assets/images/Nouvelle_sauvegarde_btn.png").convert_alpha()
        new_save_btn = pygame.transform.scale(new_save_btn, (400, 50))
        return_instruction = pygame.image.load("assets/images/return-instruction.png").convert_alpha()
        return_instruction = pygame.transform.scale(return_instruction, (125, 125))
        suppr_instruction = pygame.image.load("assets/images/suppr-instruction.png")
        suppr_instruction = pygame.transform.scale(suppr_instruction, (125, 125))

        selection_height = 0

        # On crée les pnjs
        create_all_pnjs(self)

        # Tant que le jeu tourne :
        while self.running:
            # On récupère toutes les actions de l'utilisateur
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # On ferme le jeu si l'utilisateur ferme la fenêtre
                    self.running = False
                elif event.type == pygame.KEYDOWN and self.playing is False:
                    # Dans le menu de sélection de lancement, on n'ajoute pas au dictionnaire afin d'empêcher le joueur de rester appuyé, ce qui permet de choisir sa sauvegarde plus facilement
                    if event.key == pygame.K_DOWN and selection_height < nb_sauvegardes * 100 and selection_height < 200:
                        selection_height += 100
                    elif event.key == pygame.K_UP and selection_height > 0:
                        selection_height -= 100
                    elif event.key == pygame.K_RETURN:
                        # On récupère l'élément sélectionné selon sa position et le nombre de sauvegardes présentes puis on définit la sauvegarde sur celle sélectionnée
                        if selection_height == 0:
                            self.save_selected = Database("databases/sauvegarde1.db")
                        elif selection_height == 100 and nb_sauvegardes == 1:
                            create_save(2)
                            nb_sauvegardes += 1
                            self.save_selected = Database("databases/sauvegarde2.db")
                        elif selection_height == 100 and (nb_sauvegardes == 2 or nb_sauvegardes == 3):
                            self.save_selected = Database("databases/sauvegarde2.db")
                        elif selection_height == 200 and nb_sauvegardes == 2:
                            create_save(3)
                            nb_sauvegardes += 1
                            self.save_selected = Database("databases/sauvegarde3.db")
                        elif selection_height == 200 and nb_sauvegardes == 3:
                            self.save_selected = Database("databases/sauvegarde3.db")

                        self.loaded_info = self.save_selected.get_info_joueur(0)
                        print(self.loaded_info)
                        self.player.set_coordonnees(self.loaded_info["X"], self.loaded_info["Y"])
                        self.map.switch_map(self.loaded_info["Carte"], False)
                        self.player.move("N")
                        self.player.move("S")

                        # On affiche les pnjs présents sur la map de spawn
                        for name, instance in self.pnjs.items():
                            if instance.map == self.map.zonearr:
                                self.map.add_pnj(instance, name)
                        print(self.map.pnjs_list)

                        self.playing = True  # Une fois qu'une sauvegarde a été sélectionnée ou créée, on lance le jeu
                    elif event.key == pygame.K_DELETE:
                        # On récupère l'élément sélectionné comme pour quand on presse entrée et on supprime la sauvegarde correspondante
                        if selection_height == 0:
                            delete_save(1)
                            nb_sauvegardes -= 1
                            if nb_sauvegardes == 0:  # Si c'était la dernière sauvegarde, on en crée une nouvelle
                                create_save(1)
                                nb_sauvegardes += 1
                        elif selection_height == 100 and nb_sauvegardes > 1:
                            delete_save(2)
                            nb_sauvegardes -= 1
                        elif selection_height == 200 and nb_sauvegardes == 3:
                            delete_save(3)
                            nb_sauvegardes -= 1

                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée et que le jeu tourne, on l'ajoute au dictionnaire des touches pressées
                    self.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False  # Si une touche est relâchée et que le jeu tourne, on l'enlève du dictionnaire des touches pressées

            if self.playing:  # Si on est dans le jeu
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

                # Vérifie si le joueur est en collision avec un PNJ
                for i in self.map.group:
                    if self.player.rect.colliderect(i.rect) and not isinstance(i, Player):
                        # Si oui, on effectue deux fois le mouvement inverse de celui que vient d'effectuer le joueur puis une fois le même.
                        # De cette façon, le joueur ne peut avancer et l'animation ne le montre pas comme allant dans le sens opposé à celui de la collision.
                        self.player.move(self.inverse[self.last_move])
                        self.player.move(self.inverse[self.last_move])
                        self.player.move(self.last_move)
                        # Si on appuie sur ...
                            # on vérifie si ce PNJ a une ligne de dialogue
                            # Si oui, on instancie la classe Dialogue

                # Vérifie si le joueur touche une zone qui doit le faire changer d'endroit
                for i in self.map.changes:
                    if self.player.rect.colliderect(i.rect):
                        # Si oui, on change la carte affichée en appelant la méthode switch_map() de la classe Map avec le nom de la carte associée à la collision
                        previous = self.map.zonearr
                        self.map.switch_map(i.command)
                        # On ajoute les pnjs qui doivent être sur cette carte
                        for name, instance in self.pnjs.items():
                            if instance.map == i.command:
                                self.map.add_pnj(instance, name)
                        # On retire les pnjs de la carte actuelle
                        for name, instance in self.pnjs.items():
                            if instance.map == previous:
                                self.map.remove_pnj(instance, name)
                        self.set_audio()

                # update pnjs animation
                for pnj in self.map.pnjs_list:
                    pnj[0].update()

                # Sauvegarde quand on appuie sur "*"
                if self.pressed.get(pygame.K_ASTERISK):
                    self.save_selected.sauvegarder(self.player, self.map)
                    print("Sauvegarde effectuée !")

                if self.pressed.get(pygame.K_DELETE):
                    print(self.map.zonearr, self.save_selected.get_pnj_sur_carte(self.map.zonearr))

                if self.sound_manager.get_current_theme() == (None, None):  # On lance l'audio
                    self.set_audio()

                if self.pressed.get(pygame.K_0):
                    print(self.save_selected.get_inventaire(0))
                # update map
                self.map.update()

                # update player animation
                self.player.update()

            else:  # Si on n'est pas encore dans le jeu (menu de lancement)
                # On affiche les boutons selon le nombre de sauvegardes existantes
                if self.save_selected is None and nb_sauvegardes == 1:
                    self.screen.get_display().blit(background, (0, 0))
                    self.screen.get_display().blit(save1_btn, (120, 25))
                    self.screen.get_display().blit(save_selection, (95, selection_height))
                    self.screen.get_display().blit(new_save_btn, (120, 125))
                elif self.save_selected is None and nb_sauvegardes == 2:
                    self.screen.get_display().blit(background, (0, 0))
                    self.screen.get_display().blit(save1_btn, (120, 25))
                    self.screen.get_display().blit(save_selection, (95, selection_height))
                    self.screen.get_display().blit(save2_btn, (120, 125))
                    self.screen.get_display().blit(new_save_btn, (120, 225))
                elif self.save_selected is None and nb_sauvegardes == 3:
                    self.screen.get_display().blit(background, (0, 0))
                    self.screen.get_display().blit(save1_btn, (120, 25))
                    self.screen.get_display().blit(save_selection, (95, selection_height))
                    self.screen.get_display().blit(save2_btn, (120, 125))
                    self.screen.get_display().blit(save3_btn, (120, 225))
                self.screen.get_display().blit(return_instruction, (125, 320))
                self.screen.get_display().blit(suppr_instruction, (400, 320))

            # update screen
            self.screen.update()
        pygame.quit()

    def chance_rencontre(self):
        for i in self.map.weeds:
            if self.player.lower_rect.colliderect(i.rect):
                self.alearencontre = randint(0, 100)
                if self.alearencontre < 2:
                    return True
        return False

    def set_audio(self):
        """
        Fonction qui permet de charger l'audio selon la zone dans laquelle se trouve le joueur
        """
        if "ville" in self.map.zonearr or "interieur" in self.map.zonearr:
            if self.sound_manager.get_current_theme() == (None, None):
                self.sound_manager.play("Village theme", -1)
            elif self.sound_manager.get_current_theme()[0] != "Village theme":
                self.sound_manager.transition("Village theme", -1)
        elif "route" in self.map.zonearr:
            if self.sound_manager.get_current_theme() == (None, None):
                self.sound_manager.play("Main adventure theme", -1)
            elif self.sound_manager.get_current_theme()[0] != "Main adventure theme":
                self.sound_manager.transition("Main adventure theme", -1)
        elif "pokemart" in self.map.zonearr:
            if self.sound_manager.get_current_theme() == (None, None):
                self.sound_manager.transition("PokeMart theme", -1)
            elif self.sound_manager.get_current_theme()[0] != "PokeMart theme":
                self.sound_manager.transition("PokeMart theme", -1)
        elif "pokecentre" in self.map.zonearr:
            pass
