import pygame
import os

#path=r'\\0641-SRV-FILES\perso\ELEVES_LYC\T01\LAFENETRE\Documents\TERMINALE\PROJET3_POKEMON\Pokemon-project'
#os.chdir(path)

from game import Game

pygame.init()


if __name__ == "__main__":
    game = Game()
    game.run()
