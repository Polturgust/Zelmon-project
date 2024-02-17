import sqlite3
from shutil import copy
from os import remove, rename
from os.path import exists


class Database:
    def __init__(self, path):
        self.path = path
        sqlite3.connect(path)


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
