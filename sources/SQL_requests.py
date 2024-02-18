import sqlite3
from shutil import copy
from os import remove, rename
from os.path import exists


class Database:
    def __init__(self, path):
        self.path = path
        self.database=sqlite3.connect(path)

    def get_info_joueur(self,id_joueur):
        self.c=self.database.cursor()
        self.c.execute("""SELECT * FROM Joueurs WHERE id_joueur=?""",(id_joueur,))
        self.results=self.c.fetchall()
        self.results=self.results[0]
        return {"ID":self.results[0],"Nom":self.results[1],"X":self.results[2],"Y":self.results[3],"Carte":self.results[4]}

    def get_info_pokemon(self,id_pokemon):
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Pokemons WHERE id_pokemon=?""", (id_pokemon,))
        self.results = self.c.fetchall()
        self.results=self.results[0]
        return {"ID":self.results[0],"ID_espece":self.results[1],"Nom":self.results[2],"Niveau":self.results[3],"XP":self.results[4],"PV":self.results[5],"Statut":self.results[6]}

    def get_equipe(self,id_joueur):
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_pokemon FROM Equipe WHERE id_joueur=?""", (id_joueur,))
        self.results = self.c.fetchall()
        self.a_renvoyer=[]
        for i in self.results:
            self.a_renvoyer.append(self.get_info_pokemon(i[0]))
        return self.a_renvoyer

    def get_PC(self,id_joueur):
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_pokemon FROM PC WHERE id_joueur=?""", (id_joueur,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_info_pokemon(i[0]))
        return self.a_renvoyer

    def get_attaques(self,id_pokemon):
        self.c = self.database.cursor()
        self.c.execute("""SELECT id_attaque FROM Attaques_possedees WHERE id_pokemon=?""", (id_pokemon,))
        self.results = self.c.fetchall()
        self.a_renvoyer = []
        for i in self.results:
            self.a_renvoyer.append(self.get_details_attaque(i[0]))
        return self.a_renvoyer

    def get_details_attaque(self,id_attaque):
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Attaques WHERE id_attaque=?""", (id_attaque,))
        self.results = self.c.fetchall()
        self.results=self.results[0]
        return {"ID":self.results[0],"Type":self.results[1],"Effet":self.results[2],"Degats":self.results[3],"Nom":self.results[4],"Description":self.results[5]}

    def get_details_objet(self,id_objet):
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Objets JOIN Type_objet ON Objets.id_type_objet=Type_objet.id_type_objet WHERE Objets.id_objet=? """,(id_objet,))
        self.results = self.c.fetchall()
        self.results = self.results[0]
        return {"ID":self.results[0],"ID_type_objet":self.results[1],"Type d'objet":self.results[4],"Nom":self.results[2],"Description":self.results[3],"Destinataire":self.results[6]}

    def get_inventaire(self,id_joueur):
        self.c = self.database.cursor()
        self.c.execute("""SELECT * FROM Inventaire WHERE id_joueur=? """,(id_joueur,))
        self.results = self.c.fetchall()
        self.a_renvoyer=[]
        for i in self.results:
            self.a_renvoyer.append(self.get_details_objet(i[1]))
        return self.a_renvoyer
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
    if exists(f"databases/sauvegarde{nb+1}.db"):
        rename(f"databases/sauvegarde{nb+1}.db", f"databases/sauvegarde{nb}.db")
    if exists(f"databases/sauvegarde{nb+2}.db"):
        rename(f"databases/sauvegarde{nb+2}.db", f"databases/sauvegarde{nb+1}.db")



d=Database(f"databases/base.db")
print(d.get_inventaire(0))