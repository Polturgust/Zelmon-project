import sqlite3
from shutil import copy
from os import remove, rename
from os.path import exists


class Database:
    def __init__(self, path):
        self.path = path
        self.database = sqlite3.connect(path)

    def get_info_joueur(self, id_joueur):
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Joueurs WHERE id_joueur=?""", (id_joueur,))
        self.results = self.c.fetchall()
        self.results = self.results[0]
        return {"ID": self.results[0], "Nom": self.results[1], "X": self.results[2], "Y": self.results[3],
                "Carte": self.results[4]}

    def get_info_pokemon(self, id_pokemon):
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Pokemons WHERE id_pokemon=?""", (id_pokemon,))
        self.results = self.c.fetchall()
        self.results = self.results[0]
        return {"ID": self.results[0], "ID_espece": self.results[1], "Nom": self.results[2], "Niveau": self.results[3],
                "XP": self.results[4], "PV": self.results[5], "Statut": self.results[6]}

    def get_equipe(self, id_joueur):
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_pokemon FROM Equipe WHERE id_joueur=?""", (id_joueur,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_info_pokemon(i[0]))
        return self.a_renvoyer

    def get_PC(self, id_joueur):
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_pokemon FROM PC WHERE id_joueur=?""", (id_joueur,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_info_pokemon(i[0]))
        return self.a_renvoyer

    def get_attaques(self, id_pokemon):
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_attaque FROM Attaques_possedees WHERE id_pokemon=?""", (id_pokemon,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_details_attaque(i[0]))
        return self.a_renvoyer

    def get_details_attaque(self, id_attaque):
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Attaques WHERE id_attaque=?""", (id_attaque,))
        self.results = self.c.fetchall()
        self.results = self.results[0]
        return {"ID": self.results[0], "Type": self.results[1], "Effet": self.results[2], "Degats": self.results[3],
                "Nom": self.results[4], "Description": self.results[5]}

    def get_details_objet(self, id_objet):
        self.c = self.database.cursor()
        self.c.execute(
            """SELECT * FROM Objets JOIN Type_objet ON Objets.id_type_objet=Type_objet.id_type_objet WHERE Objets.id_objet=? """,
            (id_objet,))
        self.results = self.c.fetchall()
        self.results = self.results[0]
        return {"ID": self.results[0], "ID_type_objet": self.results[1], "Type d'objet": self.results[4],
                "Nom": self.results[2], "Description": self.results[3], "Destinataire": self.results[6]}

    def get_inventaire(self, carte):
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_joueur FROM Joueurs WHERE id_joueur!=0 AND carte=? """, (carte,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_info_joueur(i[1]))
        return self.a_renvoyer

    def get_pnj_sur_carte(self, carte):
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Joueurs WHERE carte=? AND id_joueur!=0""", (carte,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_info_joueur(i[0]))
        return self.a_renvoyer

    def capturer_pokemon(self, info, id_joueur):
        self.c = self.database.cursor()
        self.c.execute("""SELECT MAX(id_pokemon) FROM Pokemons""")
        self.results = self.c.fetchall()
        self.id_pokemon = self.results[0][0] + 1
        self.a_ajouter = [self.id_pokemon]
        self.a_ajouter += [j for j in info.values()]
        self.a_ajouter = tuple(self.a_ajouter)
        self.c.execute("""INSERT INTO Pokemons VALUES (?,?,?,?,?,?,?)""", self.a_ajouter)
        self.database.commit()
        self.c.execute("""INSERT INTO PC VALUES (?,?)""", (self.id_pokemon, id_joueur))
        self.database.commit()
        print("Pokémon ajouté à la database")

    def deplacer_equipe_vers_PC(self,id_pokemon):
        self.info_pokemon=self.get_info_pokemon(id_pokemon)
        self.c.execute("""INSERT INTO PC VALUES (?,?)""",(id_pokemon,self.info_pokemon["ID"]))
        self.database.commit()
        self.c.execute("""DELETE FROM Equipe WHERE id_pokemon=?""",(id_pokemon,))
        self.database.commit()

    def deplacer_PC_vers_ID(self,id_pokemon):
        self.info_pokemon=self.get_info_pokemon(id_pokemon)
        self.c.execute("""INSERT INTO Equipe VALUES (?,?)""",(id_pokemon,self.info_pokemon["ID"]))
        self.database.commit()
        self.c.execute("""DELETE FROM PC WHERE id_pokemon=?""",(id_pokemon,))
        self.database.commit()

    def sauvegarder(self, player, map):
        self.c = self.database.cursor()
        self.c.execute("""UPDATE Joueurs SET (coord_x,coord_y,carte)=(?,?,?)""",
                       (player.pos.get()[0], player.pos.get()[1], map.zonearr))
        self.database.commit()
        print(map.zonearr, player.pos.get())


def create_save(nb):
    """
    Fonction qui permet de créer une nouvelle sauvegarde vide

    Pré-conditions :
        nb est du type integer et est compris entre 1 et 3 inclus
    Post-conditions :
        Un nouveau fichier de sauvegarde est créé
    Retourne :
        Rien.
        """
    copy("databases/base.db", f"databases/sauvegarde{nb}.db")


def delete_save(nb):
    """
    Fonction qui permet de supprimer une sauvegarde

    Pré-conditions :
        nb est tu type integer et est compris entre 1 et 3 inclus
    Post-conditions :
        Le fichier de sauvegarde correspondant est supprimé et les autres sont renommés de façon à ce que le
        numéro de sauvegarde soit le plus petit possible
    Retourne :
        Rien
    """
    remove(f"databases/sauvegarde{nb}.db")
    if exists(f"databases/sauvegarde{nb + 1}.db"):
        rename(f"databases/sauvegarde{nb + 1}.db", f"databases/sauvegarde{nb}.db")
    if exists(f"databases/sauvegarde{nb + 2}.db"):
        rename(f"databases/sauvegarde{nb + 2}.db", f"databases/sauvegarde{nb + 1}.db")


d = Database(f"databases/base.db")
print(d.get_inventaire(0))
