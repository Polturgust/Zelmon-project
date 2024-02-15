import pygame
import os
from moviepy.editor import VideoFileClip

# path=r'\\0641-SRV-FILES\perso\ELEVES_LYC\T01\LAFENETRE\Documents\TERMINALE\Pokemon-project-main'
# os.chdir(path)

from game import Game

pygame.init()
pygame.font.init()

clip = VideoFileClip("assets/videos/Pokemon Heart Gold  Opening US_480p.mp4")
clip.show()


if __name__ == "__main__":
    game = Game()
    game.run()
