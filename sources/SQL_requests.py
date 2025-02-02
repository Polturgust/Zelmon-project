import sqlite3
from shutil import copy
from os import remove, rename
from os.path import exists
from random import choices


class Database:
    def __init__(self, path):
        self.path = path
        self.database = sqlite3.connect(path)

    def get_id_joueurs(self):
        """
        Fonction qui renvoie les id de tous les id de la classe joueur
        """
        c = self.database.cursor()
        c.execute(f"""SELECT id_joueur FROM Joueurs""")
        results = c.fetchall()
        ids = [i[0] for i in results]
        return ids

    def get_info_joueur(self, id_joueur):
        """
        Récupère les informations sur le joueur depuis la base de données sous la forme :
        {"ID":Id du joueur,"Nom": Nom du joueur, "X" : coordonnée x au moment de la dernière sauvegarde,
        "Y" : coordonnée y au moment de la dernière sauvegarde, "Carte" : nom du fichier carte sur lequel le joueur
        était au moment de sauvegarder}.
        """
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Joueurs WHERE id_joueur=?""", (id_joueur,))
        self.results = self.c.fetchall()
        self.results = self.results[0]
        return {"ID": self.results[0], "Nom": self.results[1], "X": self.results[2], "Y": self.results[3],
                "Carte": self.results[4], "Image_path": self.results[5]}

    def get_info_pokemon(self, id_pokemon):
        """
        Récupère les informations sur un pokémon depuis la base de données sous la forme :
        {"ID" : ID du Pokémon, "ID_espece" : ID de son espèce, "Nom" : Nom donné à ce Pokémon,
        "Niveau" : niveau actuel du Pokémon, "XP" : nombre de points d'expérience de ce Pokémon,
        "PV" : nombre de points de vie du Pokémon, "Statut" : Eventuelle altération de statut}.
        """
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Pokemons WHERE id_pokemon=?""", (id_pokemon,))
        self.results = self.c.fetchall()
        if len(self.results) != 0:
            self.results = self.results[0]
            return {"ID": self.results[0], "ID_espece": self.results[1], "Nom": self.results[2],
                    "Niveau": self.results[3],
                    "XP": self.results[4], "PV": self.results[5], "Statut": self.results[6]}

    def get_pokemon_equipe(self, id_joueur):
        """
        Récupère le pokémon équipé par le joueur dont l'id est passé en argument

        Précondition :
            - id_joueur doit être un entier positif ou nul

        Renvoie :
            - L'ID du pokémon équipé par le joueur si le joueur a un pokémon équipé
            - None sinon
        """
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_pokemon FROM Equipe WHERE id_joueur=? AND est_equipe=1""", (id_joueur,))
        self.results = self.c.fetchall()
        if len(self.results) != 0:
            return self.results[0][0]
        return None

    def get_info_espece(self, id_espece):
        """
        Récupère les informations sur un pokémon depuis la base de données sous la forme :
        {"ID" : ID de l'espèce, "Type1" : Type princnipal, "Type2" : Type secondaire,
        "Nom" : nom de l'espèce, "Path" : chemin des images, "PV" : nombre de points de vie du Pokémon,
        "Attaque" : Stat d'attaque de base, "Defense" : Stat de défense de base,
        "Vitesse" : Stat de vitesse de base, "Courbe" : Courbe de gain de niveaux}.
        """
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Especes WHERE id_espece=?""", (id_espece,))
        self.results = self.c.fetchall()
        self.results = self.results[0]
        return {"ID_espece": self.results[0], "Nom": self.results[3], "Type1": self.results[1],
                "Type2": self.results[2], "Path": self.results[4], "PV": self.results[5], "Attaque": self.results[6],
                "Defense": self.results[7], "Vitesse": self.results[8], "Courbe": self.results[9]}

    def get_equipe(self, id_joueur):
        """
        Renvoie une liste composée des informations sur les Pokémons dans l'équipe du joueur, sous la forme d'une
        liste de dictionnaires (de la forme de ceux qui sont renvoyés par la méthode get_info_pokemon())
        """
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_pokemon FROM Equipe WHERE id_joueur=?""", (id_joueur,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_info_pokemon(i[0]))
        return self.a_renvoyer

    def get_PC(self, id_joueur):
        """
        Renvoie une liste composée des informations sur les Pokémons dans le stockage PC du joueur, sous la forme d'une
        liste de dictionnaires (de la forme de ceux qui sont renvoyés par la méthode get_info_pokemon())
        """
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_pokemon FROM PC WHERE id_joueur=?""", (id_joueur,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_info_pokemon(i[0]))
        return self.a_renvoyer

    def get_attaques(self, id_pokemon):
        """
        Renvoie une liste composée des informations sur les attaques d'un Pokémon, sous la forme d'une
        liste de dictionnaires (de la forme de ceux qui sont renvoyés par la méthode get_details_attaque())
        """
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_attaque FROM Attaques_possedees WHERE id_pokemon=?""", (id_pokemon,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_details_attaque(i[0]))
        return self.a_renvoyer

    def get_attaques_par_type(self, type1, type2=None):
        self.c = self.database.cursor()
        if type2 is not None:
            self.c.execute("""SELECT id_attaque FROM Attaques WHERE type IN (?,?)""", (type1, type2))
            self.results = self.c.fetchall()
        else:
            self.c.execute("""SELECT id_attaque FROM Attaques WHERE type=?""", (type1,))
            self.results = self.c.fetchall()
        liste = choices(self.results, k=4)
        for i in range(len(liste)):
            liste[i] = liste[i][0]
        return [self.get_details_attaque(i) for i in liste]

    def get_details_attaque(self, id_attaque):
        """
        Récupère les caractéritiques d'une attaque depuis la base de données et les renvoie sous la forme :
        {"ID" : ID de l'attaque, "Nom" : Nom de l'attaque, "Type" : type de l'attaque, "Puissance" : puissance de l'attaque,
        "Précision" : précision de l'attaque, "Effet": définit une potentielle altération de statut infligée par l'attaque,
        "Qte_effet": puissance de l'effet, "PP_max": pp maximum de l'attaque, "Description": description de l'attaque}.
        """
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Attaques WHERE id_attaque=?""", (id_attaque,))
        self.results = self.c.fetchall()
        self.results = self.results[0]
        return {"ID": self.results[0], "Nom": self.results[1], "Type": self.results[2], "Puissance": self.results[3],
                "Precision": self.results[4], "Effet": self.results[5], "Qte_effet": self.results[6],
                "Pourcent_effet": self.results[7], "PP_max": self.results[8], "Description": self.results[9]}

    def get_pp_restants(self, id_pokemon, id_attaque):
        self.c = self.database.cursor()
        self.c.execute("""SELECT pp_restant FROM Attaques_possedees WHERE id_pokemon=? and id_attaque=?""",
                       (id_pokemon, id_attaque))
        self.results = self.c.fetchall()
        if len(self.results) != 0:
            self.c.close()
            return self.results[0][0]

    def set_pp_restants(self, id_pokemon, id_attaque, pp_restants):
        """
        Procédure qui actualise les pp restants pour l'attaque dont l'ID est id_attaque pour le
        Pokemon dont l'ID est id_pokemon

        Pré-conditions :
            - id_pokemon est un entier qui correspond à l'ID d'un Pokemon
            - id_attaque est un entier qui correspond à l'ID d'une attaque possédée par le Pokemon du joueur
            - pp_restants est un entier positif qui correspond au PP restants de cette attaque
        Post-condition :
            La table Attaque_possedees est modifiée de telle sorte que les PP restants de l'attaque en question vale pp_restant
        """
        c = self.database.cursor()
        c.execute("""UPDATE Attaques_possedees SET pp_restant=? WHERE id_pokemon=? and id_attaque=? """, (pp_restants, id_pokemon, id_attaque))
        self.database.commit()

    def get_details_objet(self, id_objet):
        """
        Renvoie des détails sur un objet depuis la base de données sous la forme :
        {"ID" : ID de l'objet, "ID_type_objet" : ID du type de l'objet (est-ce un objet de soin ? Un objet à usage
        unique ? Un objet important pour l'histoire ?), "Type_objet" : Nom du type de l'objet, "Nom" : nom de l'objet,
        "Description" : description de l'objet, "Destinataire" : sur qui cet objet doit-il être utilisé ?}
        """
        self.c = self.database.cursor()
        self.c.execute(
            """SELECT * FROM Objets JOIN Type_objet ON Objets.id_type_objet=Type_objet.id_type_objet WHERE Objets.id_objet=? """,
            (id_objet,))
        self.results = self.c.fetchall()
        self.results = self.results[0]
        return {"ID": self.results[0], "ID_type_objet": self.results[1], "Type_objet": self.results[4],
                "Nom": self.results[2], "Description": self.results[3], "Destinataire": self.results[6]}

    def get_inventaire(self, ID_joueur):
        """
        Renvoie le contenu de l'inventaire d'un joueur sous la forme d'une liste de dictionnaires (eux-mêmes sous
        la forme des dictionnaires renvoyés par la méthode get_details_objet())
        """
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_objet FROM Inventaire WHERE id_joueur=?""", (ID_joueur,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_details_objet(i[0]))
        return self.a_renvoyer

    def get_pnj_sur_carte(self, carte):
        """
        Renvoie la liste des PNJ présents sur une certaine carte sous la forme d'une liste de dictionnaires (eux-mêmes
        sous la forme de ceux renvoyés par la méthode get_info_joueur())
        """
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Joueurs WHERE carte=? AND id_joueur!=0""", (carte,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_info_joueur(i[0]))
        return self.a_renvoyer

    def get_savage_pokemon(self, id_zone):
        """
        Permet de récupérer sous forme de tuple, une liste des Pokémons qui peuvent apparaître dans la zone avec leur
        coefficient d'apparition et l'id d'un Pokémon choisi aléatoirement selon ces coefficients
        """
        c = self.database.cursor()
        c.execute(f"""SELECT id_espece, coefficient_apparition FROM Apparitions WHERE id_zone={id_zone}""")
        results = c.fetchall()
        selected_pokemon = choices([i[0] for i in results], [i[1] for i in results], k=1)
        return results, selected_pokemon

    def get_current_zone(self, map):
        """
        Permet de récupérer l'id de la zone actuelle
        """
        c = self.database.cursor()
        c.execute(f"""SELECT id_zone FROM Zones WHERE {map}=1""")
        results = c.fetchall()
        return results[0][0]

    def capturer_pokemon(self, info, id_joueur):
        """
        Sauvegarde la capture d'un Pokémon par un joueur dans la base de données à partir des informations sur ce
        Pokémon (dictionnaire sous la forme de ceux renvoyés par la méthode get_info_pokemon()) et l'ID du joueur ayant
        capturé le Pokémon.
        """
        # On commence par déterminer le nouvel ID du Pokémon (le plus grand ID de la table Pokemons + 1)
        self.c = self.database.cursor()
        self.c.execute("""SELECT MAX(id_pokemon) FROM Pokemons""")
        self.results = self.c.fetchall()
        self.id_pokemon = self.results[0][0] + 1
        # On déclare les variables qui contiennent les informations à ajouter dans les différentes tables
        self.a_ajouter = [self.id_pokemon]
        self.a_ajouter += [j for j in info.values()]
        self.a_ajouter = tuple(self.a_ajouter)
        # On ajoute les données du Pokémon à la table Pokemon
        self.c.execute("""INSERT INTO Pokemons VALUES (?,?,?,?,?,?,?)""", self.a_ajouter)
        self.database.commit()
        # Puis on dirige le pokémon vers le stockage PC du joueur
        self.c.execute("""INSERT INTO PC VALUES (?,?)""", (self.id_pokemon, id_joueur))
        self.database.commit()
        return self.id_pokemon

    def deplacer_equipe_vers_PC(self, id_pokemon):
        """
        Transfère un pokémon de l'équipe du joueur à son stockage PC (ce qui se traduit par un changement de table) dans
        la base de données
        """
        # On récupère les informations sur le Pokémon, puis on les insère dans la table PC
        self.info_pokemon = self.get_info_pokemon(id_pokemon)
        self.c.execute("""INSERT INTO PC VALUES (?,?)""", (id_pokemon, self.info_pokemon["ID"]))
        self.database.commit()
        # On supprime ensuite le pokémon de la table Equipe
        self.c.execute("""DELETE FROM Equipe WHERE id_pokemon=?""", (id_pokemon,))
        self.database.commit()

    def deplacer_PC_vers_equipe(self, id_pokemon, id_joueur):
        """
        Transfère (si l'équipe du joueur n'est pas déjà pleine) un pokémon du stockage PC du joueur à son équipe
        (ce qui se traduit par un changement de table) dans la base de données.
        """
        # On commence par vérifier que le joueur n'a pas déjà 6 pokémons dans son équipe
        self.c = self.database.cursor()
        self.c.execute("""SELECT COUNT(id_pokemon) FROM Equipe WHERE id_joueur=?""", (id_joueur,))
        self.results = self.c.fetchall()
        # S'il reste de la place dans son équipe, on vérifie que le pokémon demandé n'est pas déjà dans l'équipe
        if self.results[0][0] < 6:
            self.c.execute("""SELECT id_pokemon FROM Equipe WHERE id_joueur=?""", (id_joueur,))
            self.results = self.c.fetchall()
            # Si ce n'est pas le cas, on déplace le Pokémon
            if id_pokemon not in self.results[0]:
                self.info_pokemon = self.get_info_pokemon(id_pokemon)
                self.c.execute("""INSERT INTO Equipe VALUES (?,?)""", (id_pokemon, self.info_pokemon["ID"]))
                self.database.commit()
                self.c.execute("""DELETE FROM PC WHERE id_pokemon=?""", (id_pokemon,))
                self.database.commit()
            else:
                return None
        else:
            return None

    def get_dialogue_pnj(self, ID_pnj):
        """
        Récupère une ligne de dialogue à partir de l'ID du PNJ associé
        Renvoie une chaîne de caractères contenant la ligne de dialogue
        """
        self.c.execute("""SELECT id_dialogue,condition FROM peut_parler WHERE id_joueur=?""", (ID_pnj,))
        self.results = self.c.fetchall()
        self.final = []
        for i in self.results:
            self.c.execute("""SELECT dialogue FROM Dialogues WHERE id_dialogue=?""", (i[0],))
            self.resulttemp = self.c.fetchall()
            self.final.append(self.resulttemp[0][0])
        return self.final[0]

    def get_etat_histoire(self):
        """
        INCOMPLET : A COMPLETER UNE FOIS QUE LES OBJETS CLE AURONT ETE OBTENUS
        """
        self.c.execute(
            """SELECT Inventaire.id_objet FROM Inventaire JOIN Objets ON Objets.id_objet=Inventaire.id_objet JOIN Type_objet ON Type_objet.id_type_objet=Objets.id_type_objet WHERE id_joueur=0 AND Objets.id_type_objet IN (1,2)""")
        self.results = self.c.fetchall()
        self.results = self.results
        return self.results

    def get_avantages(self, type_att, type_def):
        self.c = self.database.cursor()
        self.c.execute("""SELECT coeff FROM Avantages WHERE attaquant=? and defenseur=?""", (type_att, type_def))
        self.results = self.c.fetchall()
        return self.results[0][0]

    def sauvegarder_info_pokemon(self, info_pokemon):
        """
        Procédure qui met à jour les information du Pokemon en question dans la base de données

        Pré-condition :
            info_pokemon est un dictionnaire du même type que celui généré par get_info_pokemon()
        Post-condition :
            la bdd est mise à jour
        """
        print(info_pokemon)
        self.c = self.database.cursor()
        self.c.execute("""UPDATE Pokemons SET nom=?, niveau=?, xp=?, pv=?, alterations_statut=? WHERE id_pokemon=?""", (
        info_pokemon["Nom"], info_pokemon["Niveau"], info_pokemon["XP"],
        info_pokemon["PV"], info_pokemon["Statut"], info_pokemon["ID"]))
        self.database.commit()

    def equiper_pokemon(self, id_joueur, id_pokemon):
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_pokemon FROM Equipe WHERE id_joueur=?""", (id_joueur,))
        self.results = self.c.fetchall()
        if (id_pokemon,) in self.results:
            self.c.execute("""UPDATE Equipe SET est_equipe=0 WHERE est_equipe=1 AND id_joueur=?""", (id_joueur,))
            self.database.commit()
            self.c.execute("""UPDATE Equipe SET est_equipe=1 WHERE id_pokemon=?""", (id_pokemon,))
            self.database.commit()

    def pokecenter(self):
        self.c = self.database.cursor()
        self.c.execute(
            """SELECT Pokemons.id_pokemon FROM Pokemons JOIN Equipe ON Equipe.id_pokemon=Equipe.id_pokemon WHERE Equipe.id_joueur=0""")
        self.results = self.c.fetchall()
        for i in self.results:
            self.c.execute(
                """SELECT Especes.pv FROM Pokemons JOIN Especes ON Especes.id_espece = Pokemons.id_espece WHERE id_pokemon=?""",
                (i[0],))
            pv = self.c.fetchall()[0][0]
            self.c.execute("""UPDATE Pokemons SET pv=? WHERE id_pokemon=?""", (pv, i[0]))
            self.database.commit()

    def a_pokemons_vivants(self, id_joueur):
        self.c = self.database.cursor()
        self.c.execute(
            """SELECT Equipe.id_pokemon,pv FROM Pokemons JOIN Equipe on Equipe.id_pokemon=Pokemons.id_pokemon WHERE Equipe.id_joueur=?""",
            (id_joueur,))
        self.results = self.c.fetchall()
        liste_vivants = []
        for i in self.results:
            if i[1] > 0:
                liste_vivants.append(i[0])
        return len(liste_vivants) != 0, liste_vivants

    def sauvegarder(self, player, map, info_pokemon):
        """
        Récupère la position du joueur (coordonnées et carte sur laquelle il se trouve) pour les enregistrer dans la
        base de données.
        """
        self.c = self.database.cursor()
        self.c.execute("""UPDATE Joueurs SET (coord_x,coord_y,carte)=(?,?,?) WHERE id_joueur=0""",
                       (player.pos.get()[0], player.pos.get()[1], map.zonearr))
        self.database.commit()
        # Si les informations du Pokemon ont changé, on les met à jour dans la DB
        if len(info_pokemon) > 0:
            for pokemon in info_pokemon:
                self.sauvegarder_info_pokemon(pokemon.get_dict_infos())
                # On actualise le Pokemon sélectionné pour le combat
                if pokemon.get_selectionne() and pokemon.get_id() != self.get_pokemon_equipe(0):
                    self.equiper_pokemon(0, pokemon.get_id())
                # On met à jour les PP restants pour les attaques
                for attaque in pokemon.get_attaques():
                    self.set_pp_restants(pokemon.get_id(), attaque["ID"], attaque["PP_restants"])


def create_save(nb):
    """
    Procédure qui permet de créer une nouvelle sauvegarde vide

    Pré-conditions :
        nb est du type integer et est compris entre 1 et 3 inclus
    Post-conditions :
        Un nouveau fichier de sauvegarde est créé
        """
    copy("databases/base.db", f"databases/sauvegarde{nb}.db")


def delete_save(nb):
    """
    Procédure qui permet de supprimer une sauvegarde

    Pré-conditions :
        nb est du type integer et est compris entre 1 et 3 inclus
    Post-conditions :
        Le fichier de sauvegarde correspondant est supprimé et les autres sont renommés de façon à ce que le
        numéro de sauvegarde soit le plus petit possible
    """
    remove(f"databases/sauvegarde{nb}.db")
    if exists(f"databases/sauvegarde{nb + 1}.db"):
        rename(f"databases/sauvegarde{nb + 1}.db", f"databases/sauvegarde{nb}.db")
    if exists(f"databases/sauvegarde{nb + 2}.db"):
        rename(f"databases/sauvegarde{nb + 2}.db", f"databases/sauvegarde{nb + 1}.db")
