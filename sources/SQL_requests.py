import sqlite3
from shutil import copy


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