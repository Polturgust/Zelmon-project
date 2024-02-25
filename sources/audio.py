import pygame
import wave


class SoundManager:
    def __init__(self):
        # On définit un dictionnaire qui contient tous les sons du jeu (pas de mp3 !!)
        self.sounds = {
            "PokeMart theme": pygame.mixer.Sound("assets/audio/Ravio_s_Theme_-_The_Legend_of_Zelda__A_Link_Between_Worlds.ogg"),
            "Final Purification theme": pygame.mixer.Sound("assets/audio/Zelda_s_Lullaby_Milk_Bar_-_The_Legend_of_Zelda__A_Link_Between_Worlds.ogg"),
            "Endgame theme": pygame.mixer.Sound("assets/audio/Thieves_Hideout_The_Legend_of_Zelda_A_Link_Between_Worlds.ogg"),
            "Village theme": pygame.mixer.Sound("assets/audio/Kakariko_Village_-_The_Legend_of_Zelda__A_Link_Between_Worlds.ogg"),
            "Main adventure theme": pygame.mixer.Sound("assets/audio/Hyrule_Field_-_The_Legend_of_Zelda__A_Link_Between_Worlds.ogg"),
            "Purification theme": pygame.mixer.Sound("assets/audio/Great_Fairy_s_Fountain_Milk_Bar_-_The_Legend_of_Zelda__A_Link_Between_Worlds.ogg"),
            "Kingdom's Legend": pygame.mixer.Sound("assets/audio/A_Kingdom_s_Legend_-_The_Legend_of_Zelda__A_Link_Between_Worlds.ogg"),
            "Hyrule at peace": pygame.mixer.Sound("assets/audio/Hyrule_at_Peace_-_The_Legend_of_Zelda__A_Link_Between_Worlds.ogg"),
            "Ruined Room": pygame.mixer.Sound("assets/audio/The_Ruined_Room_-_The_Legend_of_Zelda__A_Link_Between_Worlds.ogg")
        }
        self.current_theme = None, None

    def play(self, name, loops=0):
        """
        Fonction qui permet de lancer la lecture d'un son

        Pré-conditions :
            name est une chaîne de caractères qui correspond à une clé du dictionnaire self.sounds
            loop est un integer qui correspond au nombre de fois supplémentaires pour lesquelles il faut lire le morceau (-1 lit à l'infini)
        Post-conditions :
            le son demandé est joué
        """

        self.sounds[name].play(loops=loops)
        self.current_theme = name, self.sounds[name]

    def transition(self, name, loops=0):
        """
        Fonction qui permet de transitionner entre deux thèmes

        Pré-conditions :
            name est une chaîne de caractères qui correspond à une clé du dictionnaire self.sounds
            loop est un integer qui correspond au nombre de fois supplémentaires pour lesquelles il faut lire le morceau (-1 lit à l'infini)
        Post-conditions :
            le thème actuel transitionne vers le thème suivant avec un fadeout
        """
        self.current_theme[1].fadeout(250)
        self.play(name, loops)

    def set_volume(self, name, volume):
        """
        Fonction qui permet de régler le volume d'un objet Sound

        Pré-conditions :
            name est une chaîne de caractères qui correspond à une clé du dictionnaire self.sounds
            volume est un float compris entre 0.0 et 1.0 inclus
        """
        self.sounds[name].set_volume(volume)

    def stop(self):
        """
        Fonction qui permet d'arrêter la lecture du thème actuel
        """
        self.current_theme[1].stop()
        self.current_theme = None, None

    def get_current_theme(self):
        """
        Fonction qui renvoie le thème actuel
        """
        return self.current_theme
