from pygame.mixer import Sound


class SoundManager:
    def __init__(self):
        # On définit un dictionnaire qui contient tous les sons du jeu
        self.sounds = {
            "PokeMart theme": Sound("assets/audio/Ravio_s_Theme_-_The_Legend_of_Zelda__A_Link_Between_Worlds.mp3"),
            "Final Purification theme": Sound("assets/audio/Zelda_s_Lullaby_Milk_Bar_-_The_Legend_of_Zelda__A_Link_Between_Worlds.mp3"),
            "Endgame theme": Sound("assets/audio/Thieves_Hideout_The_Legend_of_Zelda_A_Link_Between_Worlds.mp3"),
            "Village theme": Sound("assets/audio/Kakariko_Village_-_The_Legend_of_Zelda__A_Link_Between_Worlds.mp3"),
            "Main adventure theme": Sound("assets/audio/Hyrule_Field_-_The_Legend_of_Zelda__A_Link_Between_Worlds.mp3"),
            "Purification theme": Sound("assets/audio/Great_Fairy_s_Fountain_Milk_Bar_-_The_Legend_of_Zelda__A_Link_Between_Worlds.mp3"),
            "Kingdom's Legend": Sound("assets/audio/A_Kingdom_s_Legend_-_The_Legend_of_Zelda__A_Link_Between_Worlds.mp3"),
            "Hyrule at peace": Sound("assets/audio/Hyrule_at_Peace_-_The_Legend_of_Zelda__A_Link_Between_Worlds.mp3"),
            "Ruined Room": Sound("assets/audio/The_Ruined_Room_-_The_Legend_of_Zelda__A_Link_Between_Worlds.mp3")
        }

    def play(self, name):
        """
        Fonction qui permet de lancer la lecture d'un son

        Pré-conditions :
            name est une chaîne de caractères qui correspond à une clé du dictionnaire self.sounds
        Post-conditions :
            le son demandé est joué
        """
        self.sounds[name].play()
