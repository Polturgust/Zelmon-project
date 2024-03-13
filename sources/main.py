import pygame
import os

# path=r'\\0641-SRV-FILES\perso\ELEVES_LYC\T01\LAFENETRE\Documents\TERMINALE\Pokemon-project-main'
# os.chdir(path)

from game import Game

pygame.init()
pygame.font.init()

game = Game()
game.run()