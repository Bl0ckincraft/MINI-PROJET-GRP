import math
import time

from PIL import Image, ImageTk

# Une variable qui peut augmenter la résolution des drapeaux.
# Par défaut : SIZE_MULTIPLIER = 1
# /!\ Attention certains drapeaux en haute résolution peuvent être long à charger /!\
SIZE_MULTIPLIER = 1
# Une variable qui permet d'afficher ou non les temps de réalisation des drapeaux dans la console.
# Par défaut : TIME_LOGS = False
TIME_LOGS = True


# Il s'agit d'une classe utilitaire pour pouvoir faire des calculs de position avec un cercle (notament savoir si un
# point P(x; y) est à l'intérieur).
class Circle:
    def getBiggestX(self):
        return self.centerX + self.radius

    def getBiggestY(self):
        return self.centerY + self.radius

    def getSmallestX(self):
        return self.centerX - self.radius

    def getSmallestY(self):
        return self.centerY - self.radius

    def __init__(self, centerX: int, centerY: int, radius: int):
        """
        Constructeur classique de la classe.

        :param centerX: Coordonnée x du centre du cercle.
        :param centerY: Coordonnée y du center du cercle.
        :param radius: Rayon du cercle.
        """

        self.centerX = centerX
        self.centerY = centerY
        self.radius = radius

    def isLocationIn(self, x: int, y: int):
        """
        On vérifie si le point P(x; y) se trouve dans le cercle.

        :param x: Coordonnée x du point.
        :param y: Coordonnée y du point.
        :return: Si le point se trouve dans le cercle.
        """

        # Pour éviter des calculs inutiles
        if x < self.getSmallestX() or x > self.getBiggestX() or y < self.getSmallestY() or y > self.getBiggestY():
            return False

        return (x - self.centerX)**2 + (y - self.centerY)**2 <= self.radius**2


# Il s'agit d'une classe utilitaire pour pouvoir faire des calculs de position avec un anneau (notament savoir si un
# point P(x; y) est à l'intérieur).
class Ring:
    def __init__(self, centerX: int, centerY: int, outRadius: int, inRadius: int):
        """
        Constructeur classique de la classe.

        :param centerX: Coordonnée x du centre de l'anneau.
        :param centerY: Coordonnée y du center du l'anneau.
        :param outRadius: Rayon extérieur de l'anneau.
        :param inRadius: Rayon intérieur de l'anneau.
        """

        self.outCircle = Circle(centerX, centerY, outRadius)
        self.inCircle = Circle(centerX, centerY, inRadius)

    def isLocationIn(self, x: int, y: int):
        """
        On vérifie si le point P(x; y) se trouve dans l'anneau.
        Pour cela on vérifie que le point se trouve bien dans le cercle extérieur mais pas dans le cercle intérieur.

        :param x: Coordonnée x du point.
        :param y: Coordonnée y du point.
        :return: Si le point se trouve dans l'anneau.
        """
        return self.outCircle.isLocationIn(x, y) and not self.inCircle.isLocationIn(x, y)


# Il s'agit d'une classe utilitaire pour pouvoir faire des calculs de position avec un triangle (notament savoir si un
# point P(x; y) est à l'intérieur).
class Triangle:
    def getBiggestX(self):
        return max(self.x1, self.x2, self.x3)

    def getBiggestY(self):
        return max(self.y1, self.y2, self.y3)

    def getSmallestX(self):
        return min(self.x1, self.x2, self.x3)

    def getSmallestY(self):
        return min(self.y1, self.y2, self.y3)

    def getArea(self):
        """
        Calcul de l'aire du triangle, on en a besoin pour savoir si un point P(x; y) est à l'intérieur.

        :return: l'aire du triangle.
        """

        return abs(0.5 * ((self.x1 * self.y2 + self.x2 * self.y3 + self.x3 * self.y1) - (self.y1 * self.x2 + self.y2 * self.x3 + self.y3 * self.x1)))

    def __init__(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        """
        Constructeur classique de la classe.

        :param x1: Coordonnée x du premier point.
        :param y1: Coordonnée y du premier point.
        :param x2: Coordonnée x du deuxième point.
        :param y2: Coordonnée y du deuxième point.
        :param x3: Coordonnée x du troisième point.
        :param y3: Coordonnée y du troisième point.
        """

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def isLocationIn(self, x: int, y: int):
        """
        On vérifie si le point P(x; y) se trouve dans le triangle.
        Pour cela, on calcul la somme de l'aire de trois triangle formé à partir de deux points du triangle actuel et du
        point P(x; y), ainsi si la somme de ces aires est égal à l'aire du triangle actuel alors le point se trouve bien
        dans le triangle.

        :param x: Coordonnée x du point.
        :param y: Coordonnée y du point.
        :return: Si le point se trouve dans le triangle.
        """

        # Pour éviter des calculs inutiles
        if x < self.getSmallestX() or x > self.getBiggestX() or y < self.getSmallestY() or y > self.getBiggestY():
            return False

        return Triangle(self.x1, self.y1, self.x2, self.y2, x, y).getArea() + Triangle(self.x1, self.y1, x, y, self.x3, self.y3).getArea() + Triangle(x, y, self.x2, self.y2, self.x3, self.y3).getArea() == self.getArea()


# Il s'agit d'une classe utilitaire pour pouvoir faire des calculs de position avec une étoile (notament savoir si un
# point P(x; y) est à l'intérieur).
class Star:
    def __init__(self, centerX: int, centerY: int, nearRadius: int, farRadius: int, rotation: float):
        """
        Constructeur classique de la classe.

        :param centerX: Coordonnée x du centre de l'étoile.
        :param centerY: Coordonnée y du centre de l'étoile.
        :param nearRadius: Rayon du cercle le plus petit.
        :param farRadius: Rayon du cercle le plus grand.
        :param rotation: Rotation de l'étoile.
        """

        # L'étoile est constitué de 5 triangles que l'on génère par compréhension à l'aide du cercle trigonométrique et
        # du module math. (Dans ce module, les angles pour le sinus et le cosinus doivent être en radians.)
        self.triangles = [
            Triangle(
                # On cast les résultats en integers car sinon l'étoile n'est pas bien formée probablement à cause des
                # arrondis.
                int(math.cos((340 + i * 360 / 5 + rotation) / 180 * math.pi) * nearRadius) + centerX,
                int(math.sin((340 + i * 360 / 5 + rotation) / 180 * math.pi) * nearRadius) + centerY,
                int(math.cos((200 + i * 360 / 5 + rotation) / 180 * math.pi) * nearRadius) + centerX,
                int(math.sin((200 + i * 360 / 5 + rotation) / 180 * math.pi) * nearRadius) + centerY,
                int(math.cos((90 + i * 360 / 5 + rotation) / 180 * math.pi) * farRadius) + centerX,
                int(math.sin((90 + i * 360 / 5 + rotation) / 180 * math.pi) * farRadius) + centerY,
            ) for i in range(5)
        ]

    def isLocationIn(self, x: int, y: int):
        """
        On vérifie si le point P(x; y) se trouve dans l'étoile.
        Pour cela, on vérifie si le point est dans un des triangles qui composent l'étoile.

        :param x: Coordonnée x du point.
        :param y: Coordonnée y du point.
        :return: Si le point se trouve dans l'étoile.
        """

        for triangle in self.triangles:
            if triangle.isLocationIn(x, y):
                return True

        return False


# Il s'agit d'une classe utilitaire pour pouvoir faire des calculs de position avec l'icone de l'Inde (notament savoir
# si un point P(x; y) est à l'intérieur).
class IndiaIcon:
    def __init__(self, centerX: int, centerY: int, width: int):
        """
        Constructeur classique de la classe.

        :param centerX: la coordonnée x du centre de l'icone.
        :param centerY: la coordonnée y du centre de l'icone.
        :param width: la taille de l'icone (soit le périmètre du cercle extérieur)
        """
        self.shapes = [
            Ring(centerX, centerY, int(width / 2), int(width * (200 / 230) / 2)),
            Circle(centerX, centerY, int(width * (40 / 230) / 2))
        ]

        self.shapes.extend([
            Circle(
                centerX + int(math.cos((360 / 24 * (i + 0.5)) / 180 * math.pi) * (width * (200 / 230) / 2)),
                centerY + int(math.sin((360 / 24 * (i + 0.5)) / 180 * math.pi) * (width * (200 / 230) / 2)),
                int(width * (12 / 230) / 2)
            ) for i in range(24)
        ])

        self.shapes.extend([
            Triangle(
                centerX + int(math.cos((360 / 24 * i) / 180 * math.pi) * (width * (40 / 230) / 2)),
                centerY + int(math.sin((360 / 24 * i) / 180 * math.pi) * (width * (40 / 230) / 2)),
                centerX + int(math.cos((360 / 24 * (i + 0.3)) / 180 * math.pi) * (width * (82 / 230) / 2)),
                centerY + int(math.sin((360 / 24 * (i + 0.3)) / 180 * math.pi) * (width * (82 / 230) / 2)),
                centerX + int(math.cos((360 / 24 * (i - 0.3)) / 180 * math.pi) * (width * (82 / 230) / 2)),
                centerY + int(math.sin((360 / 24 * (i - 0.3)) / 180 * math.pi) * (width * (82 / 230) / 2)),
            ) for i in range(24)
        ])

        self.shapes.extend([
            Triangle(
                centerX + int(math.cos((360 / 24 * i) / 180 * math.pi) * (width * (194 / 230) / 2)),
                centerY + int(math.sin((360 / 24 * i) / 180 * math.pi) * (width * (194 / 230) / 2)),
                centerX + int(math.cos((360 / 24 * (i + 0.3)) / 180 * math.pi) * (width * (82 / 230) / 2)),
                centerY + int(math.sin((360 / 24 * (i + 0.3)) / 180 * math.pi) * (width * (82 / 230) / 2)),
                centerX + int(math.cos((360 / 24 * (i - 0.3)) / 180 * math.pi) * (width * (82 / 230) / 2)),
                centerY + int(math.sin((360 / 24 * (i - 0.3)) / 180 * math.pi) * (width * (82 / 230) / 2)),
            ) for i in range(24)
        ])

    def isLocationIn(self, x: int, y: int):
        """
        On vérifie si le point P(x; y) se trouve dans l'icone.
        Pour cela, on vérifie si le point est dans une des formes qui composent l'icone.

        :param x: Coordonnée x du point.
        :param y: Coordonnée y du point.
        :return: Si le point se trouve dans l'icone.
        """

        for shape in self.shapes:
            if shape.isLocationIn(x, y):
                return True

        return False


# Cette fonction renvoie le drapeau du pays demandé ou None si le drapeau n'est pas implémenté.
def getFlag(name: str):
    # On génère le nom de la fonction associé au drapeau avec le format suivant : "make[NomDuPays]Flag".
    # Avec ce fonctionnement, on rend le code plus maintenable puisqu'il suffit de créer une nouvelle fonction pour
    # implémenter un nouveau drapeau sans avoir à modifier celle-ci.
    functionName = f"make{name.title().replace(' ', '')}Flag"

    # On vérifie que la fonction existe.
    if functionName in globals():
        # On renvoie le résultat de la fonction transformé en image tkinter.
        return ImageTk.PhotoImage(image=eval(f"{functionName}()"), size=(600, 300))


finlandFlag = None


# Une fonction pour faire le drapeau de la Finlande avec PIL sans utiliser de formes prédéfinies.
def makeFinlandFlag():
    # Pour calculer le temps de réalisation
    start = time.time()


    # Import de la variable globale finlandFlag.
    global finlandFlag
    # S'il a déja été fait durant cette instance de l'application, on ne le refait pas et donc on n'entre pas dans le
    # if.
    if finlandFlag is None:
        # Création de l'image vide.
        flag = Image.new("RGB", (600 * SIZE_MULTIPLIER, 300 * SIZE_MULTIPLIER))

        # Coloration de l'image.
        for x in range(600 * SIZE_MULTIPLIER):
            for y in range(300 * SIZE_MULTIPLIER):
                if 165 * SIZE_MULTIPLIER < x <= 266 * SIZE_MULTIPLIER or 99 * SIZE_MULTIPLIER < y <= 200 * SIZE_MULTIPLIER:
                    flag.putpixel((x, y), (0, 47, 108))
                else:
                    flag.putpixel((x, y), (255, 255, 255))

        # Sauvegarde de l'image pour ne pas la recréer durant la même instance de l'application.
        finlandFlag = flag

    # Pour afficher le temps de réalisation
    if TIME_LOGS:
        print(f"Le drapeau a pris {time.time() - start} secondes pour être réalisé.")

    # On renvoie le drapeau.
    return finlandFlag


czechRepublicFlag = None


# Une fonction pour faire le drapeau de la Tchéquie avec PIL sans utiliser de formes prédéfinies.
def makeCzechRepublicFlag():
    # Pour calculer le temps de réalisation
    start = time.time()


    # Import de la variable globale czechRepublicFlag.
    global czechRepublicFlag
    # S'il a déja été fait durant cette instance de l'application, on ne le refait pas et donc on n'entre pas dans le
    # if.
    if czechRepublicFlag is None:
        # Création de l'image vide.
        flag = Image.new("RGB", (600 * SIZE_MULTIPLIER, 300 * SIZE_MULTIPLIER))

        # Création de l'objet utilitaire pour réaliser le triangle bleu du drapeau.
        blueTriangle = Triangle(0 * SIZE_MULTIPLIER, 0 * SIZE_MULTIPLIER, 223 * SIZE_MULTIPLIER, 150 * SIZE_MULTIPLIER, 0 * SIZE_MULTIPLIER, 299 * SIZE_MULTIPLIER)

        # Coloration de l'image.
        for x in range(600 * SIZE_MULTIPLIER):
            for y in range(300 * SIZE_MULTIPLIER):
                if blueTriangle.isLocationIn(x, y):
                    flag.putpixel((x, y), (17, 69, 126))
                elif y < 150 * SIZE_MULTIPLIER:
                    flag.putpixel((x, y), (255, 255, 255))
                else:
                    flag.putpixel((x, y), (215, 20, 26))

        # Sauvegarde de l'image pour ne pas la recréer durant la même instance de l'application.
        czechRepublicFlag = flag

    # Pour afficher le temps de réalisation
    if TIME_LOGS:
        print(f"Le drapeau a pris {time.time() - start} secondes pour être réalisé.")

    # On renvoie le drapeau.
    return czechRepublicFlag


togoFlag = None


# Une fonction pour faire le drapeau du Togo avec PIL sans utiliser de formes prédéfinies.
def makeTogoFlag():
    # Pour calculer le temps de réalisation
    start = time.time()


    # Import de la variable globale togoFlag.
    global togoFlag
    # S'il a déja été fait durant cette instance de l'application, on ne le refait pas et donc on n'entre pas dans le
    # if.
    if togoFlag is None:
        # Création de l'image vide.
        flag = Image.new("RGB", (600 * SIZE_MULTIPLIER, 300 * SIZE_MULTIPLIER))

        # Création de l'objet utilitaire pour réaliser l'étoile blanche du drapeau.
        whiteStar = Star(90 * SIZE_MULTIPLIER, 90 * SIZE_MULTIPLIER, 20 * SIZE_MULTIPLIER, 60 * SIZE_MULTIPLIER, 180)

        # Coloration de l'image.
        for x in range(600 * SIZE_MULTIPLIER):
            for y in range(300 * SIZE_MULTIPLIER):
                if whiteStar.isLocationIn(x, y):
                    flag.putpixel((x, y), (255, 255, 255))
                elif x < 180 * SIZE_MULTIPLIER and y < 180 * SIZE_MULTIPLIER:
                    flag.putpixel((x, y), (210, 16, 52))
                elif (y // (60 * SIZE_MULTIPLIER)) % 2 == 0:
                    flag.putpixel((x, y), (0, 106, 78))
                else:
                    flag.putpixel((x, y), (255, 206, 0))

        # Sauvegarde de l'image pour ne pas la recréer durant la même instance de l'application.
        togoFlag = flag

    # Pour afficher le temps de réalisation
    if TIME_LOGS:
        print(f"Le drapeau a pris {time.time() - start} secondes pour être réalisé.")

    # On renvoie le drapeau.
    return togoFlag


indiaFlag = None


# Une fonction pour faire le drapeau de l'Inde avec PIL sans utiliser de formes prédéfinies.
def makeIndiaFlag():
    # Pour calculer le temps de réalisation
    start = time.time()


    # Import de la variable globale indiaFlag.
    global indiaFlag
    # S'il a déja été fait durant cette instance de l'application, on ne le refait pas et donc on n'entre pas dans le
    # if.
    if indiaFlag is None:
        # Création de l'image vide.
        flag = Image.new("RGB", (600 * SIZE_MULTIPLIER, 300 * SIZE_MULTIPLIER))

        # Création de l'objet utilitaire pour réaliser l'icone bleu du drapeau.
        blueIndiaIcon = IndiaIcon(300 * SIZE_MULTIPLIER, 150 * SIZE_MULTIPLIER, 80 * SIZE_MULTIPLIER)

        # Coloration de l'image.
        for x in range(600 * SIZE_MULTIPLIER):
            for y in range(300 * SIZE_MULTIPLIER):
                if blueIndiaIcon.isLocationIn(x, y):
                    flag.putpixel((x, y), (0, 0, 88))
                elif y < 100 * SIZE_MULTIPLIER:
                    flag.putpixel((x, y), (255, 153, 51))
                elif y < 200 * SIZE_MULTIPLIER:
                    flag.putpixel((x, y), (255, 255, 255))
                else:
                    flag.putpixel((x, y), (19, 138, 8))

        # Sauvegarde de l'image pour ne pas la recréer durant la même instance de l'application.
        indiaFlag = flag

    # Pour afficher le temps de réalisation
    if TIME_LOGS:
        print(f"Le drapeau a pris {time.time() - start} secondes pour être réalisé.")

    # On renvoie le drapeau.
    return indiaFlag


frenchFlag = None


def makeFranceFlag():
    # Pour calculer le temps de réalisation
    start = time.time()


    # Import de la variable globale indiaFlag.
    global frenchFlag
    # S'il a déja été fait durant cette instance de l'application, on ne le refait pas et donc on n'entre pas dans le
    # if.
    if frenchFlag is None:
        # Création de l'image vide.
        flag = Image.new("RGB", (600 * SIZE_MULTIPLIER, 300 * SIZE_MULTIPLIER))

        # Coloration de l'image.
        for x in range(600 * SIZE_MULTIPLIER):
            for y in range(300 * SIZE_MULTIPLIER):
                if x < 200 * SIZE_MULTIPLIER:
                    flag.putpixel((x, y), (0, 0, 255))
                elif x < 400 * SIZE_MULTIPLIER:
                    flag.putpixel((x, y), (255, 255, 255))
                else:
                    flag.putpixel((x, y), (255, 0, 0))

        # Sauvegarde de l'image pour ne pas la recréer durant la même instance de l'application.
        frenchFlag = flag

    # Pour afficher le temps de réalisation
    if TIME_LOGS:
        print(f"Le drapeau a pris {time.time() - start} secondes pour être réalisé.")

    # On renvoie le drapeau.
    return frenchFlag
