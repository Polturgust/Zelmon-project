import pygame


# Classe pour gérer les Pokemons et leurs infos durant les sessions de jeu.
# Les sauvegardes doivent être faites avec ces informations
class Pokemon:
    def __init__(self, game, info):
        self.game = game

        # Informations du dictionnaire généré par get_info_pokemon() -> à renvoyer dans sauvegarder_info_pokemon()
        self.id = info["ID"]
        self.id_espece = info["ID_espece"]
        self.nom = info["Nom"]
        self.niveau = info["Niveau"]
        self.xp = info["XP"]
        self.pv = info["PV"]
        self.statut = info["Statut"]

        # Le Pokemon en question est-il celui qui combat ?
        self.selectionne = False

        # Quelles sont les attaques du Pokemon ?
        self.attaques = list()
        self.info_attaques = list()

    def get_id(self):
        """Fonction qui renvoie l'id du Pokémon"""
        return self.id

    def get_id_espece(self):
        """Fonction qui renvoie l'id de l'espèce du Pokemon"""
        return self.id_espece

    def get_nom(self):
        """Fonction qui renvoie le nom du Pokemon"""
        return self.nom

    def get_niveau(self):
        """Fonction qui renvoie le niveau actuel du Pokemon"""
        return self.niveau

    def get_xp(self):
        """Fonction qui renvoie la quantité d'XP du Pokemon"""
        return self.xp

    def set_xp(self, amount):
        """
        Procédure qui définit la quantité d'XP du Pokemon comme égale à amount

        Pré-condition :
            amount est un nombre
        """
        self.xp = amount

    def get_pv(self):
        """Fonction qui renvoie le nombre de PV du Pokemon"""
        return self.pv

    def set_pv(self, nb):
        """
        Procédure qui définit le nombre de PV du Pokemon comme égal à nb

        Pré-condition :
            nb est un entier
        """
        self.pv = nb

    def get_statut(self):
        """Fonction qui renvoie les altérations de statut du Pokemon"""
        return self.statut

    def set_statut(self, statut):
        """
        Procédure qui définit le statut du Pokemon comme "statut"

        Pré-condition :
            statut est une chaine de caractères qui correspond à un statut du jeu
        """

    def get_dict_infos(self):
        """Fonction qui renvoie un dictionnaire de la même forme que celui généré par getr_info_pokemon()"""
        return {"ID": self.id, "ID_espece": self.id_espece, "Nom": self.nom, "Niveau": self.niveau, "XP": self.xp, "PV": self.pv, "Statut": self.statut}

    def get_selectionne(self):
        """Fonction qui renvoie True si le Pokemon est celui qui combat, False sinon"""
        return self.selectionne

    def set_selectionne(self, boolean):
        """
        Procédure qui permet de définir si le Pokemon est celui qui combat

        Pré-condition :
            boolean est un boolean qui vaut True si le Pokemon est celui qui combat, False sinon
        """
        self.selectionne = boolean

    def get_attaques(self):
        """
        Fonction qui renvoie les attaques du Pokemon sous la forme d'une liste de dictionnaire de la forme
        {"ID": id_attaque, "PP_restants": pp_restants}
        """
        return self.attaques

    def get_info_attaques(self):
        """
        Fonction qui renvoie les informations des attaques du Pokemon sous la forme donnée par la fonction
        get_attaques du fichier SQL_requests.py
        """
        return self.info_attaques

    def get_nb_attaques(self):
        """Fonction qui renvoie le nombre d'attaques du Pokemon"""
        return len(self.attaques)

    def add_attaque(self, id_att, pp):
        """
        Procédure qui ajoute une attaque à la liste self.attaques

        Pré-conditions :
            - id est un entier qui correspond à l'id de l'attaque à ajouter
            - pp est un entier positif ou nul qui correspond aux pp restants de cette attaque
        """
        self.attaques.append({"ID": id_att, "PP_restants": pp})
        self.info_attaques.append(self.game.save_selected.get_details_attaque(id_att))

    def reset_pp(self, attack):
        """
        Procédure qui définit les pp d'une attaque comme égaux à pp

        Pré-conditions :
            attack est un entier qui correspond à l'ID de l'attaque en question
        Post-conditions :
            Les pp de l'attaque sont restaurés à leur maximum
        """
        trouve = False
        i = 0
        while i < len(self.attaques) and not trouve:
            if attack == self.attaques[i]["ID"]:
                self.attaques[i]["PP_restants"] = self.info_attaques[i]["PP_max"]
                trouve = True
            i += 1

    def decrease_pp(self, attack):
        """
        Procédure qui baisse de 1 les pp restants de l'attaque spécifiée

        Pré-condition :
            attack est un entier qui correspond à l'ID de l'attaque en question
        Post-condition :
            les pp restants de cette attaque sont décrémentés de 1
        """
        trouve = False
        i = 0
        while i < len(self.attaques) and not trouve:
            if attack == self.attaques[i]["ID"]:
                self.attaques[i]["PP_restants"] -= 1
                trouve = True
            i += 1


def has_living_pokemon(team):
    """
    Fonction qui renvoie une liste des Pokemon non K.O. dans l'équipe du joueur

    Pré-conditions :
        - team est une liste (ou un tuple) d'instances de la classe Pokemon
        - chaque élément de la liste correspond à un Pokemon de l'équipe du joueur
    Renvoie :
        - un tuple des Pokemon encore en vie
        - False si tous sont K.O.
    """
    living = list()
    for pokemon in team:
        if pokemon.get_pv() > 0:
            living.append(pokemon)
    if len(living) > 0:
        living = (element for element in living)
    else:
        living = False
    return living

