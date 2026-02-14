import pygame.rect

import SQL_requests


class Dialogue:
    def __init__(self, dialogue, screen, map, combat=None):
        self.textedonne = dialogue
        self.screen = screen
        self.map = map
        self.texte = []
        self.combat = combat
        while len(self.textedonne) > 45:
            self.texte.append(self.textedonne[:45])
            self.textedonne = self.textedonne[45:]
        self.texte.append(self.textedonne)
        self.pressed = {}
        self.cooldown = 0

    def afficher(self, update_map=True):
        """
        Méthode afficher():

        Affiche le dialogue dans une fenêtre en bas de l'écran, s'arrangeant pour séparer le dialogue en
        plusieurs morceaux s'il est trop long.

        Valeurs en entrée :
            - Aucune

        Préconditions :
            - Aucune

        Valeur renvoyée :
            - Aucune

        Post-conditions :
            - Aucune
        """
        # On va parcourir la liste contenant les parties du dialogue : On initialise donc un indice de départ à 0
        i = 0
        # Tant que l'on n'est pas au bout de la liste, on récupère les actions de l'utilisateur
        while i < len(self.texte):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False

            # S'il reste au moins deux lignes de texte à afficher, on les affiche
            if len(self.texte) - i >= 2:
                self.surface = pygame.Surface((self.screen.get_size()[0], 100))
                self.surface.fill((255, 255, 255))
                if update_map:
                    self.screen.update()
                    self.map.update()
                if self.combat is not None:
                    self.combat.afficher()

                self.screen.get_display().blit(self.surface, (0, self.screen.get_size()[1] - 150))
                self.screen.get_display().blit(
                    pygame.font.SysFont('Comic Sans MS', 20).render(self.texte[i], False, (0, 0, 0)),
                    (40, self.screen.get_display().get_size()[1] - 140))
                self.screen.get_display().blit(
                    pygame.font.SysFont('Comic Sans MS', 20).render(self.texte[i + 1], False, (0, 0, 0)),
                    (40, self.screen.get_display().get_size()[1] - 90))

            # Sinon, on n'affiche qu'une seule ligne (très probablement la dernière)
            else:
                self.surface = pygame.Surface((self.screen.get_size()[0], 100))
                self.surface.fill((255, 255, 255))
                if update_map:
                    self.screen.update()
                    self.map.update()
                if self.combat is not None:
                    self.combat.afficher()
                self.screen.get_display().blit(self.surface, (0, self.screen.get_size()[1] - 150))
                self.screen.get_display().blit(
                    pygame.font.SysFont('Comic Sans MS', 20).render(self.texte[i], False, (0, 0, 0)),
                    (40, self.screen.get_display().get_size()[1] - 120))
            # Pour éviter que le dialogue ne passe trop vite si l'on laisse appuyée la touche entrée, on crée un
            # compteur qui empêche le passage à la ligne suivante avant 0.5 seconde
            # S'il n'est pas à 0, il décroît d'une unité
            if self.cooldown > 0:
                self.cooldown -= 1
            # Si le temps est écoulé et que le joueur presse la touche entrée, on ajoute deux à notre indice pour
            # pouvoir relancer une itération de la boucle avec les lignes de texte suivantes
            if self.pressed.get(pygame.K_RETURN) and self.cooldown <= 0:
                i += 2
                self.cooldown = 30
