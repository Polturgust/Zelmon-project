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

        self.tmx_data = None # Contiendra le fichier carte utilisable par pygame
        self.map_layer = None # Contiendra les données de la couche que l'on affiche
        self.group = None # Contiendra le groupe de lutins permettant de centrer l'écran sur le joueur
        self.map_data = None # Contiendra les données du fichier carte utilisables par pyscroll
        self.zonearr = None # Contiendra la zone d'origine du joueur (pour le changement de carte)
        self.changes = None # Contiendra les collisions
        self.collisions = None # Contiendra les collisions qui font changer le joueur de carte

        # Lance le jeu sur la carte donnée (sera adapté plus tard)
        self.switch_map("ville0")

    def switch_map(self, map):
        # load the wanted map
        self.tmx_data = pytmx.load_pygame(f"assets\\map\\{map}.tmx")
        # get the map for pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        # render the mapdata
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.screen.get_size(), zoom=2)
        # puts everything together
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=20)
        self.map_layer._x_offset = 240

        self.group.add(self.player)

        # print(self.tmx_data.objects)
        # Crée deux groupe de lutins pyscroll, un qui contiendra les collisions, l'autre les changements de carte
        self.collisions = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.changes = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.weeds=pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

        # Pour chaque couche de la carte actuelle :
        for i in self.tmx_data.visible_layers:

            # Si la couche est un groupe d'objets Tiled :
            if isinstance(i, pytmx.TiledObjectGroup):
                # Pour chaque objet de cette couche :
                for j in i:
                    # Si c'est un objet de la couche qui contient les collisions, on crée une collision et on l'ajoute au groupe collisions
                    if i.name == "collisions":
                        self.collisions.add(Collisions(j.width, j.height, j.x, j.y, ""))

                    # Si c'est un objet de la couche qui contient les changements de carte, on crée une collision et on l'ajoute au groupe des changements de carte
                    if i.name == "changements_de_map":
                        if j.name != None and "vers_route" in j.name:
                            dest = j.name.split("vers_route")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "route" + dest[1]))
                        elif j.name != None and "vers_ville" in j.name:
                            dest=j.name.split("vers_ville")
                            self.changes.add(Collisions(j.width, j.height, j.x, j.y, "ville" + dest[1]))


                    # Si c'est un objet de la couche qui contient les points d'apparitions, on choisit le bon en fonction de la zone de laquelle le joueur arrive
                    if i.name == "points_de_spawn":
                        print(self.zonearr, j.name)
                        # Si le nom correspond à la zone d'où vient le joueur, on déplace le joueur vers cette zone
                        if self.zonearr != None and self.zonearr in j.name:
                            self.player.rect.x, self.player.rect.y = j.x, j.y
                            self.player.pos = Vector(j.x, j.y)
                            self.player.move("S")
                            self.player.move("N")
                        # Sinon, si le joueur ne vient de nulle part (ex après avoir chargé une sauvegarde), on le place à l'endroit d'apparition par défaut
                        elif self.zonearr == None and j.name == "spawn_default":
                            self.player.rect.x, self.player.rect.y = j.x, j.y
                            self.player.pos = Vector(j.x, j.y)
                            self.player.move("S")
                            self.player.move("N")

                    if i.name=="herbes":
                        self.weeds.add(Collisions(j.width,j.height,j.x,j.y,""))


        # On change la zone d'origine du joueur à la zone actuelle
        self.zonearr = map
        # On centre le groupe du joueur sur le joueur
        self.group.center(self.player.pos.get())

    def update(self):
        # show the map on screen with the player centered
        self.group.center(self.player.pos.get())
        self.group.draw(self.screen.get_display())


    def get_size(self):
        """
        Renvoie la taille de la map en pixel dans un tuple
        """
        return self.map_data.map_size[0] * 16, self.map_data.map_size[1] * 16
