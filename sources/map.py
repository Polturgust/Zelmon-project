import pygame
import pytmx
import pyscroll
from collisions import Collisions
from vector import Vector


class Map:
    def __init__(self, screen, player):
        # On crée des attributs pour les valeurs données en arguments
        self.screen = screen
        self.player = player

        # On initialise les différentes variables utiles :

        self.tmx_data = None  # Contiendra le fichier carte utilisable par pygame
        self.map_layer = None  # Contiendra les données de la couche que l'on affiche
        self.group = None  # Contiendra le groupe de lutins permettant de centrer l'écran sur le joueur
        self.pnjs_list = list()
        self.map_data = None  # Contiendra les données du fichier carte utilisables par pyscroll
        self.zonearr = None  # Contiendra la zone d'origine du joueur (pour le changement de carte)
        self.changes = None  # Contiendra les collisions
        self.collisions = None  # Contiendra les collisions qui font changer le joueur de carte
        self.weeds = None  # Contiendra les hautes herbes
        self.ice = None  # Contiendra la glace
        self.moovers = None  # Contiendra les plaques mouvantes

    def switch_map(self, map, forcer_apparition=True):
        """
        Fonction qui permet de changer de carte

        Pré-conditions :
            map correspond au nom d'une carte au format .tmx et présente dans le dossier assets/map
        Post-conditions :
            la carte affichée à l'écran est modifiée
        """
        # load the wanted map
        self.tmx_data = pytmx.load_pygame(f"assets\\map\\{map}.tmx")
        # get the map for pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        # render the mapdata
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.screen.get_size(), zoom=2)
        # puts everything together
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=11)
        self.map_layer._x_offset = 240

        self.group.add(self.player)

        # Crée deux groupes de lutins pyscroll, un qui contiendra les collisions, l'autre les changements de carte
        self.collisions = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=11)
        self.changes = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=11)
        # Crée un groupe qui contient les hautes herbes → quand un Pokémon sauvage peut apparaître
        self.weeds = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=11)
        # Crée un groupe pour le sol glacé
        self.ice = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=11)
        # Crée un groupe pour les plaques mouvantes
        self.moovers = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=11)

        # Pour chaque couche de la carte actuelle :
        for i in self.tmx_data.visible_layers:
            # Si la couche est un groupe d'objets Tiled :
            if isinstance(i, pytmx.TiledObjectGroup):
                # Pour chaque objet de cette couche :
                for j in i:
                    # Si c'est un objet de la couche qui contient les collisions, on crée une collision et on l'ajoute au groupe collisions
                    if i.name == "collisions":
                        self.collisions.add(Collisions(j.width, j.height, j.x, j.y, ""))
                    # Si c'est un objet de la couche qui contient les bloqueurs, on crée une collision et on passe en commande le sens dans lequel on peut passer
                    if i.name == "bloqueurs":
                        self.collisions.add(Collisions(j.width, j.height, j.x, j.y, j.name))

                    # Si c'est un objet de la couche qui contient les changements de carte, on crée une collision et on l'ajoute au groupe des changements de carte
                    if i.name == "changements_de_map":
                        if j.name is not None and "vers_route" in j.name:
                            dest = j.name.split("vers_route")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "route" + dest[1]))
                        elif j.name is not None and "vers_ville" in j.name:
                            dest = j.name.split("vers_ville")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "ville" + dest[1]))
                        elif j.name is not None and "vers_interieur_simple" in j.name:
                            dest = j.name.split("vers_interieur_simple")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "interieur_simple" + dest[1]))
                        elif j.name is not None and "vers_interieur_grand" in j.name:
                            dest = j.name.split("vers_interieur_grand")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "interieur_grand" + dest[1]))
                        elif j.name is not None and "vers_pokecentre" in j.name:
                            dest = j.name.split("vers_pokecentre")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "pokecentre" + dest[1]))
                        elif j.name is not None and "vers_pokemart" in j.name:
                            dest = j.name.split("vers_pokemart")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "pokemart" + dest[1]))
                        elif j.name is not None and "vers_interieur_mc_chambre" in j.name:
                            dest = j.name.split("vers_interieur_mc_chambre")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "interieur_mc_chambre" + dest[1]))
                        elif j.name is not None and "vers_interieur_mc_salon" in j.name:
                            dest = j.name.split("vers_interieur_mc_salon")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "interieur_mc_salon" + dest[1]))
                        elif j.name is not None and "vers_interieur_prof" in j.name:
                            dest = j.name.split("vers_interieur_prof")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "interieur_prof" + dest[1]))
                        elif j.name is not None and "vers_temple_of_purification" in j.name:
                            dest = j.name.split("vers_temple_of_purification")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "temple_of_purification" + dest[1]))
                        elif j.name is not None and "vers_arene" in j.name:
                            dest = j.name.split("vers_arene")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "arene" + dest[1]))

                    # Si c'est un objet de la couche qui contient les points d'apparitions, on choisit le bon en fonction de la zone de laquelle le joueur arrive
                    if i.name == "points_de_spawn" and forcer_apparition:
                        print(self.zonearr, j.name)
                        # Si le nom correspond à la zone d'où vient le joueur, on déplace le joueur vers cette zone
                        if self.zonearr is not None and self.zonearr in j.name:
                            self.player.rect.x, self.player.rect.y = j.x, j.y
                            self.player.pos = Vector(j.x, j.y)
                            self.player.move("N")
                            self.player.move("S")
                        # Sinon, si le joueur ne vient de nulle part (ex après avoir chargé une sauvegarde), on le place à l'endroit d'apparition par défaut
                        elif self.zonearr is None and j.name == "spawn_default":
                            self.player.rect.x, self.player.rect.y = j.x, j.y
                            self.player.pos = Vector(j.x, j.y)
                            self.player.move("N")
                            self.player.move("S")

                    if i.name == "herbes":
                        self.weeds.add(Collisions(j.width, j.height, j.x, j.y, ""))

                    if i.name == "glace":
                        self.ice.add(Collisions(j.width, j.height, j.x, j.y, ""))

                    if i.name == "moovers":
                        self.moovers.add(Collisions(j.width, j.height, j.x, j.y, j.name))

        # On change la zone d'origine du joueur à la zone actuelle
        self.zonearr = map
        # On centre le groupe du joueur sur le joueur
        self.group.center(self.player.pos.get())

    def add_pnj(self, pnj, name):
        """
        Fonction qui permet d'ajouter un PNJ au groupe pnjs afin de l'afficher à l'écran

        Pré-conditions :
            pnj est une instance de PNJ ou d'une de ses classes filles
            name est une string qui correspond au nom du pnj
        Post-conditions :
            le pnj a bien été ajouté au groupe et sera affiché lors du prochain appel de la fonction update
        """
        self.group.add(pnj)  # On ajoute le pnj au groupe pour qu'il soit affiché à l'écran
        # On le fait bouger pour qu'il n'apparaisse pas en haut à gauche puis on lui remet sa position initiale
        base_direction = pnj.animation.direction
        pnj.move("N")
        pnj.move("S")
        pnj.animation.direction = base_direction
        # On ajoute le pnj à la liste des pnjs présents sur la carte
        self.pnjs_list.append((pnj, name))
        print("pnj ajouté")

    def remove_pnj(self, pnj, name):
        """
        Fonction qui permet de retirer un pnj du groupe afin qu'il ne soit pas affiché à l'écran

        Pré-conditions :
            pnj est une instance de PNJ ou d'une de ses classes filles
            name est une string qui correspond au nom du pnj
        Post-conditions :
            le pnj est retiré du groupe et de la liste des pnjs à l'écran
        """
        self.group.remove(pnj)
        print(pnj, name)
        self.pnjs_list.remove((pnj, name))
        print("pnj retiré")

    def update(self):
        """
        Fonction qui affiche la carte à l'écran avec le joueur centré
        """
        self.group.center(self.player.pos.get())  # on centre la carte sur le joueur
        self.group.draw(self.screen.get_display())  # on affiche la carte

    def get_size(self):
        """
        Renvoie la taille de la map en pixel dans un tuple
        """
        return self.map_data.map_size[0] * 16, self.map_data.map_size[1] * 16
