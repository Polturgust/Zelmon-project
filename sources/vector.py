import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def magnitude(self):
        """
        Renvoie la norme du vecteur
        """
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        """
        Permet de normaliser le vecteur
        """
        mag = self.magnitude
        if mag != 0:
            self.x /= mag
            self.y /= mag

    @staticmethod
    def dot(vector1, vector2):
        """
        Permet d'effectuer un produit scalaire
        """
        if isinstance(vector1, Vector) and isinstance(vector2, Vector):
            return vector1.x * vector2.x + vector1.y * vector2.y

    # Operators overloads
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        return Vector(other.x - self.x, other.y - self.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.x

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def get(self):
        """
        Renvoie les coordonnées sous forme de tuple
        """
        return self.x, self.y

