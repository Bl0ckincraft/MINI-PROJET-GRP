import math

from PIL import Image, ImageTk


# Il s'agit d'une classe utilitaire pour pouvoir faire des calculs de position avec un triangle (notament savoir si un
# point P(x; y) est à l'intérieur).
class Triangle:
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
        return Triangle(self.x1, self.y1, self.x2, self.y2, x, y).getArea() + Triangle(self.x1, self.y1, x, y, self.x3, self.y3).getArea() + Triangle(x, y, self.x2, self.y2, self.x3, self.y3).getArea() == self.getArea()


# Il s'agit d'une classe utilitaire pour pouvoir faire des calculs de position avec une étoile (notament savoir si un
# point P(x; y) est à l'intérieur).
class Star:
    def __init__(self, xCenter: int, yCenter: int, nearRadius: int, farRadius: int, rotation: float):
        """
        Constructeur classique de la classe.

        :param xCenter: Coordonnée x du centre de l'étoile.
        :param yCenter: Coordonnée y du centre de l'étoile.
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
                int(math.cos((340 + i * 360 / 5 + rotation) / 180 * math.pi) * nearRadius) + xCenter,
                int(math.sin((340 + i * 360 / 5 + rotation) / 180 * math.pi) * nearRadius) + yCenter,
                int(math.cos((200 + i * 360 / 5 + rotation) / 180 * math.pi) * nearRadius) + xCenter,
                int(math.sin((200 + i * 360 / 5 + rotation) / 180 * math.pi) * nearRadius) + yCenter,
                int(math.cos((90 + i * 360 / 5 + rotation) / 180 * math.pi) * farRadius) + xCenter,
                int(math.sin((90 + i * 360 / 5 + rotation) / 180 * math.pi) * farRadius) + yCenter,
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
    # Import de la variable globale finlandFlag.
    global finlandFlag
    # S'il a déja été fait durant cette instance de l'application, on ne le refait pas et donc on n'entre pas dans le
    # if.
    if finlandFlag is None:
        # Création de l'image vide.
        flag = Image.new("RGB", (600, 300))

        # Coloration de l'image.
        for x in range(600):
            for y in range(300):
                if 165 < x <= 266 or 99 < y <= 200:
                    flag.putpixel((x, y), (0, 47, 108))
                else:
                    flag.putpixel((x, y), (255, 255, 255))

        # Sauvegarde de l'image pour ne pas la recréer durant la même instance de l'application.
        finlandFlag = flag

    # On renvoie le drapeau.
    return finlandFlag


czechRepublicFlag = None


# Une fonction pour faire le drapeau de la Tchéquie avec PIL sans utiliser de formes prédéfinies.
def makeCzechRepublicFlag():
    # Import de la variable globale czechRepublicFlag.
    global czechRepublicFlag
    # S'il a déja été fait durant cette instance de l'application, on ne le refait pas et donc on n'entre pas dans le
    # if.
    if czechRepublicFlag is None:
        # Création de l'image vide.
        flag = Image.new("RGB", (600, 300))

        # Création de l'objet utilitaire pour réaliser le triangle bleu du drapeau.
        blueTriangle = Triangle(0, 0, 223, 150, 0, 299)

        # Coloration de l'image.
        for x in range(600):
            for y in range(300):
                if blueTriangle.isLocationIn(x, y):
                    flag.putpixel((x, y), (17, 69, 126))
                elif y < 150:
                    flag.putpixel((x, y), (255, 255, 255))
                else:
                    flag.putpixel((x, y), (215, 20, 26))

        # Sauvegarde de l'image pour ne pas la recréer durant la même instance de l'application.
        czechRepublicFlag = flag

    # On renvoie le drapeau.
    return czechRepublicFlag


togoFlag = None


# Une fonction pour faire le drapeau du Togo avec PIL sans utiliser de formes prédéfinies.
def makeTogoFlag():
    # Import de la variable globale togoFlag.
    global togoFlag
    # S'il a déja été fait durant cette instance de l'application, on ne le refait pas et donc on n'entre pas dans le
    # if.
    if togoFlag is None:
        # Création de l'image vide.
        flag = Image.new("RGB", (600, 300))

        # Création de l'objet utilitaire pour réaliser l'étoile blanche du drapeau.
        whiteStar = Star(90, 90, 20, 60, 180)

        # Coloration de l'image.
        for x in range(600):
            for y in range(300):
                if whiteStar.isLocationIn(x, y):
                    flag.putpixel((x, y), (255, 255, 255))
                elif x < 180 and y < 180:
                    flag.putpixel((x, y), (210, 16, 52))
                elif (y // 60) % 2 == 0:
                    flag.putpixel((x, y), (0, 106, 78))
                else:
                    flag.putpixel((x, y), (255, 206, 0))

        # Sauvegarde de l'image pour ne pas la recréer durant la même instance de l'application.
        togoFlag = flag

    # On renvoie le drapeau.
    return togoFlag
