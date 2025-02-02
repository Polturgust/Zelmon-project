from random import randint, choice
from moviepy.editor import *
import os

from screen import Screen
from map import Map
from player import Player
from combat import Combat
from pnj import *
from SQL_requests import *
from dialogue import *
from audio import SoundManager
from pokemon import Pokemon


class Game:
    def __init__(self):
        # set the game to running
        self.running = True
        self.playing = False
        # initialise the screen
        self.screen = Screen()
        # create a player
        self.player = Player(self)
        # create future list to store player's team of Pokemons
        self.player_poke_info = None
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
        # on crée un dictionnaire qui contient les touches pressées (permet de rester appuyé sur une touche → utile
        # pour se déplacer)
        self.pressed = dict()

        self.cooldown = 0  # cooldown pour l'apparition des pokemon

        self.save_selected = None  # Une sauvegarde est-elle sélectionnée ?

        self.joystick = None

    def run(self):
        # Lance la vidéo d'introduction au lancement du jeu → appuyer sur Esc permet d'interrompre la vidéo
        VideoFileClip("assets/videos/The Legend of Pokemon Zelda's Corruption slow audio.mp4").preview()

        # On vérifie si on a des sauvegardes, sinon on crée une sauvegarde nommée sauvegarde1
        nb_sauvegardes = len(os.listdir("databases")) - 1

        if nb_sauvegardes == 0:
            create_save(1)
            nb_sauvegardes += 1

        # On importe et modifie les images de l'écran de lancement
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

        # Tant que le jeu tourne :
        while self.running:
            # On récupère toutes les actions de l'utilisateur
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # On ferme le jeu si l'utilisateur ferme la fenêtre
                    self.running = False
                # ----------------------- Start screen logic ----------------------- #
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

                        # On load sur la bonne map et au bon emplacement
                        self.loaded_info = self.save_selected.get_info_joueur(0)
                        self.player.set_coordonnees(self.loaded_info["X"], self.loaded_info["Y"])
                        self.map.switch_map(self.loaded_info["Carte"], False)
                        self.player.move("N")
                        self.player.move("S")

                        self.create_player_poke_info()

                        # On crée les PNJs
                        create_all_pnjs(self)

                        # On affiche les pnjs présents sur la map de spawn
                        for name, instance in self.pnjs.items():
                            if instance.map == self.map.zonearr:
                                self.map.add_pnj(instance, name)

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
                    self.pressed[
                        event.key] = False  # Si une touche est relâchée et que le jeu tourne, on l'enlève du dictionnaire des touches pressées

            if self.playing:  # Si on est dans le jeu
                # ------------------------------------------------------------ Player movement ------------------------------------------------------------ #
                if event.type == pygame.JOYDEVICEADDED:
                    self.joystick = pygame.joystick.Joystick(event.device_index)

                if self.player.get_slipping_status() is False and self.player.get_moover_effect() is None:
                    # sans le -30 on peut sortir de l'écran je pense que c'est dû à la largeur du joueur (ses coordonnées sont le point en haut à gauche)
                    if self.pressed.get(pygame.K_UP) and self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[1] > 0 and self.player.pos.get()[0] < self.map.map_data.map_size[0] * 16 - 30:
                        self.player.move("NE")
                        self.last_move = "NE"
                        self.player.set_moving_status(True)
                        if self.cooldown != 0:
                            self.cooldown -= 1
                        if self.player.get_ice_status():
                            self.player.set_slipping_status(True)

                    elif self.pressed.get(pygame.K_UP) and self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[
                        1] > 0 and \
                            self.player.pos.get()[0] > 0:
                        self.player.move("NW")
                        self.last_move = "NW"
                        self.player.set_moving_status(True)
                        if self.cooldown != 0:
                            self.cooldown -= 1
                        if self.player.get_ice_status():
                            self.player.set_slipping_status(True)

                    elif self.pressed.get(pygame.K_DOWN) and self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[
                        1] < \
                            self.map.map_data.map_size[1] * 16 - 30 and self.player.pos.get()[0] < \
                            self.map.map_data.map_size[0] * 16 - 30:
                        self.player.move("SE")
                        self.last_move = "SE"
                        self.player.set_moving_status(True)
                        if self.cooldown != 0:
                            self.cooldown -= 1
                        if self.player.get_ice_status():
                            self.player.set_slipping_status(True)

                    elif self.pressed.get(pygame.K_DOWN) and self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[
                        1] < \
                            self.map.map_data.map_size[1] * 16 - 30 and self.player.pos.get()[0] > 0:
                        self.player.move("SW")
                        self.last_move = "SW"
                        self.player.set_moving_status(True)
                        if self.cooldown != 0:
                            self.cooldown -= 1
                        if self.player.get_ice_status():
                            self.player.set_slipping_status(True)

                    elif self.pressed.get(pygame.K_UP) and self.player.pos.get()[1] > 0:
                        self.player.move("N")
                        self.last_move = "N"
                        self.player.set_moving_status(True)
                        if self.cooldown != 0:
                            self.cooldown -= 1
                        if self.player.get_ice_status():
                            self.player.set_slipping_status(True)

                    elif self.pressed.get(pygame.K_DOWN) and self.player.pos.get()[1] < self.map.map_data.map_size[
                        1] * 16 - 30:
                        self.player.move("S")
                        self.last_move = "S"
                        self.player.set_moving_status(True)
                        if self.cooldown != 0:
                            self.cooldown -= 1
                        if self.player.get_ice_status():
                            self.player.set_slipping_status(True)

                    elif self.pressed.get(pygame.K_LEFT) and self.player.pos.get()[0] > 0:
                        self.player.move("W")
                        self.last_move = "W"
                        self.player.set_moving_status(True)
                        if self.cooldown != 0:
                            self.cooldown -= 1
                        if self.player.get_ice_status():
                            self.player.set_slipping_status(True)

                    elif self.pressed.get(pygame.K_RIGHT) and self.player.pos.get()[0] < self.map.map_data.map_size[
                        0] * 16:
                        self.player.move("E")
                        self.last_move = "E"
                        self.player.set_moving_status(True)
                        if self.cooldown != 0:
                            self.cooldown -= 1
                        if self.player.get_ice_status():
                            self.player.set_slipping_status(True)
                    
                    elif self.joystick is not None:
                        joy_x, joy_y = self.joystick.get_axis(0), self.joystick.get_axis(1)
                        joy_dir = ""
                        if joy_y < -0.2:
                            joy_dir += "N"
                        elif joy_y > 0.2:
                            joy_dir += "S"
                        if joy_x < -0.2:
                            joy_dir += "W"
                        elif joy_x > 0.2:
                            joy_dir += "E"

                        if len(joy_dir) == 0:
                            self.player.set_moving_status(False)
                        else:
                            self.player.move(joy_dir)
                            self.last_move = joy_dir
                            self.player.set_moving_status(True)
                            if self.cooldown != 0:
                                self.cooldown -= 1
                            if self.player.get_ice_status():
                                self.player.set_slipping_status(True)
                            
                    else:
                        self.player.set_moving_status(False)

                elif self.player.get_slipping_status() is True:
                    self.player.move(self.last_move)

                elif self.player.get_moover_effect() is not None:
                    self.player.move(self.player.get_moover_effect())

                else:
                    self.player.set_moving_status(False)


                # ------------------------------------------------------------ Fight ------------------------------------------------------------ #
                # Déclenche un combat
                if self.cooldown == 0:
                    if self.chance_rencontre():
                        origin = self.map.zonearr
                        self.save_selected.get_current_zone(origin)
                        self.map.switch_map("combat")
                        # On remove les PNJs de la carte
                        for name, instance in self.pnjs.items():
                            if instance.map == origin:
                                self.map.remove_pnj(instance, name)
                        self.set_audio()
                        self.reset_pressed_keys()
                        combat = Combat(self, self.screen, self.player, self.map, origin, self.save_selected)
                        # Si le combat est perdu, on remet le joueur dans sa chambre.
                        if combat.combat_sauvage(self.save_selected.get_savage_pokemon(self.save_selected.get_current_zone(origin))[1][0]) is False:
                            print("On vou téléporte dans votre chambre")
                            self.map.switch_map("interieur_mc_chambre0")
                            self.player.pos = Vector(185, 139)
                            self.player.move("W")
                            self.player.move("E")
                            print("Vos pokemon sont soignés")
                            print(self.map.zonearr)
                            self.pokecenter()  # On soigne les Pokemon du joueur
                        self.cooldown = 120

                        # On remet les PNJs de la carte
                        for name, instance in self.pnjs.items():
                            if instance.map == self.map.zonearr:
                                self.map.add_pnj(instance, name)
                        self.set_audio()

                # ------------------------------------------------------------ Collisions ------------------------------------------------------------ #

                # Vérifie si le joueur est en collision avec un élément du décor
                for i in self.map.collisions:
                    if self.player.rect.colliderect(i.rect) and not isinstance(i, Player) and i.command == "":
                        # Si oui, on effectue deux fois le mouvement inverse de celui que vient d'effectuer le joueur puis une fois le même.
                        # De cette façon, le joueur ne peut avancer et l'animation ne le montre pas comme allant dans le sens opposé à celui de la collision.
                        self.player.move(self.inverse[self.last_move])
                        self.player.move(self.inverse[self.last_move])
                        self.player.move(self.last_move)

                        self.player.set_slipping_status(False)  # Si on est en collision, on ne glisse plus
                        self.player.set_moover_effect(None)  # Si on est en collision, on ne subit plus l'effet de la plaque

                    # Si c'est un bloqueur qui permet d'aller vers le bas
                    elif self.player.rect.colliderect(i.rect) and not isinstance(i, Player) and i.command == "bas":
                        # On vérifie que le joueur se dirige bien vers le bas selon son dernier mouvement
                        if self.last_move == "S" or self.last_move == "SE" or self.last_move == "SW":
                            pass
                        # Sinon, on le bloque
                        else:
                            self.player.move(self.inverse[self.last_move])
                            self.player.move(self.inverse[self.last_move])
                            self.player.move(self.last_move)
                        self.player.set_moover_effect(None)  # Si on est en collision, on ne subit plus l'effet de la plaque
                    # On fait la même chose avec les trois autres directions
                    elif self.player.rect.colliderect(i.rect) and not isinstance(i, Player) and i.command == "gauche":
                        if self.last_move == "W" or self.last_move == "SW" or self.last_move == "NW":
                            pass
                        else:
                            self.player.move(self.inverse[self.last_move])
                            self.player.move(self.inverse[self.last_move])
                            self.player.move(self.last_move)
                        self.player.set_moover_effect(None)  # Si on est en collision, on ne subit plus l'effet de la plaque
                    elif self.player.rect.colliderect(i.rect) and not isinstance(i, Player) and i.command == "droit":
                        if self.last_move == "E" or self.last_move == "SE" or self.last_move == "NE":
                            pass
                        else:
                            self.player.move(self.inverse[self.last_move])
                            self.player.move(self.inverse[self.last_move])
                            self.player.move(self.last_move)
                        self.player.set_moover_effect(None)  # Si on est en collision, on ne subit plus l'effet de la plaque

                # Vérifie si le joueur est en collision avec un PNJ
                for i in self.map.group:
                    if self.player.rect.colliderect(i.rect) and not isinstance(i, Player):
                        # Si oui, on effectue deux fois le mouvement inverse de celui que vient d'effectuer le joueur puis une fois le même.
                        # De cette façon, le joueur ne peut avancer et l'animation ne le montre pas comme allant dans le sens opposé à celui de la collision.
                        self.player.move(self.inverse[self.last_move])
                        self.player.move(self.inverse[self.last_move])
                        self.player.move(self.last_move)

                        # Vérifie si le joueur veut parler à un PNJ
                        # (Pour l'instant, le dialogue est choisi aléatoirement)
                        if self.pressed[pygame.K_RETURN]:
                            # On stoppe les déplacements du joueur
                            self.reset_pressed_keys()
                            liste_dialogues = [
                                "Bonjour ! Comment ça va ? J'espère que tu    passes une bonne journée !",
                                "C'est vraiment super que tu sois là, tu es un vrai rayon de soleil !",
                                "Quelle est la réponse à la question de la    vie, de l'univers, et du reste ?",
                                "Comme tu as grandi depuis la dernière fois   que je t'ai vu !",
                                "Oh ! Un petit bonhomme vert ! Parles-tu notre langue ?",
                                "Je n'avais plus d'idées de dialogue, imaginez une conversation :-/",
                                "Hey bonjour ! Je t'attendais ! Figure toi que j'ai une histoire de dingue à te raconter : hier, j'ai croisé un chat, et il se trouve   que ce chat eh ben c'était le chat de mon    voisin qui se trouve être un chien mais il l'a toujours appelé un chat et je trouve cette    histoire fort cocasse et ce dialogue avait juste pour but de te faire perdre du temps <3",
                                "Aparemment, il y aurait un chat bizarre qui a trouvé son chemin jusuqu'au bout du monde...",
                                "Savais-tu que tu peux appuyer sur A pour fuir un combat ?",
                                "Si jamais tu es perdu, c'est dommage.",
                                "Mange bien cinq fruits et légumes par jour   pour rester en bonne santé !",
                                "ATCHOUM ! Excuse-moi, je crois que je suis   allergique aux bonhommes verts...",
                                "SELECT FROM Dialogue WHERE is_dialogue_useful=False... Oups, tu étais là ? Je faisais un  peu de poésie moderne...",
                                "Et si j'étais seulement un personnage non    joueur dans un jeu développé par trois       lycéens ? Ce serait terrifiant.",
                                "J'ai pas d'idée de dialogue -un grand homme, 28 mars 2023.",
                                "Le savais-tu ? 90% des dialogues sont        inutiles. Et 100% de ce message est faux."]

                            Dialogue(choice(liste_dialogues), self.screen, self.map).afficher()

                # Vérifie si le joueur touche une zone qui doit le faire changer d'endroit
                for i in self.map.changes:
                    if self.player.rect.colliderect(i.rect):
                        # Si oui, on change la carte affichée en appelant la méthode switch_map() de la classe Map avec le nom de la carte associée à la collision
                        previous = self.map.zonearr
                        self.map.switch_map(i.command)
                        self.update_map_pnj(previous, i)
                        self.set_audio()

                # Vérifie si le joueur est sur de la glace
                touches_ice = None
                for i in self.map.ice:
                    if self.player.lower_rect.colliderect(i.rect):
                        # Si oui, on définit le joueur comme étant sur de la glace
                        self.player.set_ice_status(True)
                        touches_ice = True
                if touches_ice is None:
                    self.player.set_ice_status(False)
                    self.player.set_slipping_status(False)

                # Vérifie si le joueur est sur un moover
                for i in self.map.moovers:
                    if self.player.lower_rect.colliderect(i.rect):
                        # Si oui, on définit le joueur comme étant sur un moover et on précise sa direction
                        if i.command == "bas":
                            self.player.set_moover_effect("S")
                        if i.command == "haut":
                            self.player.set_moover_effect("N")
                        if i.command == "droite":
                            self.player.set_moover_effect("E")
                        elif i.command == "gauche":
                            self.player.set_moover_effect("W")


                # ------------------------------------------------------------ Miscellaneous ------------------------------------------------------------ #
                # update pnjs animation
                """
                for pnj in self.map.pnjs_list:
                    pnj[0].update()
                """

                # Si le joueur est dans un Pokecentre, on soigne son équipe (car pas de NPC ni potions pour le moment)
                if "pokecentre" in self.map.zonearr:
                    self.pokecenter()

                # Sauvegarde quand on appuie sur "S"
                if self.pressed.get(pygame.K_s):
                    self.save_selected.sauvegarder(self.player, self.map, self.player_poke_info)
                    self.pressed[pygame.K_s] = False
                    Dialogue("Sauvegarde effectuée !", self.screen, self.map).afficher()

                if self.sound_manager.get_current_theme() == (None, None):  # On lance l'audio
                    self.set_audio()

                # Met à jour la carte
                self.map.update()

                # Anime le joueur
                self.player.update()

            # ------------------------------------------------------------ Start screen interface ------------------------------------------------------------ #
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
                alearencontre = randint(0, 100)
                if alearencontre < 2:
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
                self.sound_manager.play("PokeMart theme", -1)
            elif self.sound_manager.get_current_theme()[0] != "PokeMart theme":
                self.sound_manager.transition("PokeMart theme", -1)
        elif "pokecentre" in self.map.zonearr:
            if self.sound_manager.get_current_theme() == (None, None):
                self.sound_manager.play("Pokecentre theme", -1)
            elif self.sound_manager.get_current_theme()[0] != "Pokecentre theme":
                self.sound_manager.transition("Pokecentre theme", -1)
        elif "temple_of_purification" in self.map.zonearr:
            if self.sound_manager.get_current_theme() == (None, None):
                self.sound_manager.play("Purification theme", -1)
            elif self.sound_manager.get_current_theme()[0] != "Purification theme":
                self.sound_manager.transition("Purification theme", -1)
        elif "combat" in self.map.zonearr:
            if self.sound_manager.get_current_theme() == (None, None):
                self.sound_manager.play("Wild battle theme", -1)
            elif self.sound_manager.get_current_theme()[0] != "combat":
                self.sound_manager.transition("Wild battle theme", -1)

    def reset_pressed_keys(self):
        """
        Fonction qui remet toutes les touches pressées à "False"

        Post-conditions :
            self.pressed a toutes ses valeurs sur False
        """
        for key in self.pressed:
            self.pressed[key] = False

    def update_map_pnj(self, previous, i):
        """
        Fonction qui met à jour les PNJs présents sur la carte
        → On enlève les PNJs de la carte précédente et on ajoute ceux de la carte actuelle

        Post-condition :
            Les PNJs affichés sur la carte sont les bons
        """
        # On retire les pnjs de la carte actuelle
        for name, instance in self.pnjs.items():
            if instance.map == previous:
                self.map.remove_pnj(instance, name)
        # On ajoute les pnjs qui doivent être sur cette carte
        for name, instance in self.pnjs.items():
            if instance.map == i.command:
                self.map.add_pnj(instance, name)

    def get_player_poke_info_list(self):
        """
        Fonction qui renvoie la liste "player_poke_info" qui contient les instances de la classe Pokemon des
        différents Pokemon du joueur
        """
        return self.player_poke_info

    def create_player_poke_info(self):
        """
        Procédure qui permet de créer et remplir la liste player_poke_info avec les informations initiales
        des Pokemons de l'équipe du joueur
        """
        # On crée des instances de Pokemon pour tous les membres de l'équipe
        self.player_poke_info = [Pokemon(self, info) for info in self.save_selected.get_equipe(0)]

        # On regarde lequel est le Pokemon équipé pour combattre afin de le définir comme tel
        pokemon_equipe = self.save_selected.get_pokemon_equipe(0)
        i = 0
        trouve = False
        while i < len(self.player_poke_info) and not trouve:
            if self.player_poke_info[i].get_id() == pokemon_equipe:
                trouve = True
                self.player_poke_info[i].set_selectionne(True)
            i += 1

        # On définit leurs attaques et leurs pp_restants
        for pokemon in self.player_poke_info:
            for attaque in self.save_selected.get_attaques(pokemon.get_id()):
                pokemon.add_attaque(attaque["ID"], self.save_selected.get_pp_restants(pokemon.get_id(), attaque["ID"]))

    def set_specific_poke_info(self, index, pokemon):
        """
        Procédure qui permet de modifier un élément de la liste "player_poke_info"

        Pré-conditions :
            - index est un entier compris entre 0 et len(self.player_poke_info) - 1
            - pokemon est une instance de la classe Pokemon du fichier pokemon.py

        Post-condition :
            l'élément à l'indice "index" de la liste est remplacé par la valeur spécifiée
        """
        self.player_poke_info[index] = pokemon

    def add_to_player_poke_info(self, pokemon):
        """
        Procédure qui permet d'ajouter un élément à la fin de la liste "player_poke_info"

        Pré-condition :
            pokemon est une instance de la classe Pokemon du fichier pokemon.py
        Post-condition :
            pokemon est ajouté à la fin de la liste
        """
        self.player_poke_info.append(pokemon)

    def pokecenter(self):
        """
        Procédure qui restaure les PV et PP des Pokemons présents dans la liste player_poke_info
        """
        for pokemon in self.player_poke_info:
            pokemon.set_pv(self.save_selected.get_info_espece(pokemon.get_id_espece())["PV"])
            for attaque in pokemon.get_attaques():
                pokemon.reset_pp(attaque["ID"])
