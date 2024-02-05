import pygame


class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def image_at(self, rectangle):
        """
        Fonction appelée par images (voir ci-dessous) qui crée l'image en elle-même.
        Une fois le spritesheet découpé par la fonction images, cette fonction crée un rectangle transparent de la bonne taille
        et y peint une des images du spritesheet.
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()  # Creer une image transparente de la taille du rectangle
        image.blit(self.sheet, (0, 0), rect)  # Peindre une partie du spritesheet sur l'image
        return image

    def images(self, rows, columns):
        """
        Fonction qui découpe le spritesheet en lignes et en colonnes et enregistre chaque image crée par la fonction image_at dans une liste.
        La classe Animation peut ensuite utiliser cette liste pour faire défiler les images et donner une illusion de mouvement
        """
        xStep = self.sheet.get_width()/columns
        yStep = self.sheet.get_height()/rows
        cropped_images = []
        for xi in range(columns):
            for yi in range(rows):
                x = xi*xStep
                y = yi*yStep
                cropped_images.append(self.image_at(pygame.Rect(x, y, xStep, yStep)))
        return cropped_images
