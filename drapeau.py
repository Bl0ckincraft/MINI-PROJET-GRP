import math

from PIL import Image, ImageTk


class Triangle:
    def getArea(self):
        return abs(0.5 * ((self.x1 * self.y2 + self.x2 * self.y3 + self.x3 * self.y1) - (self.y1 * self.x2 + self.y2 * self.x3 + self.y3 * self.x1)))

    def __init__(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def isLocationIn(self, x: int, y: int):
        return Triangle(self.x1, self.y1, self.x2, self.y2, x, y).getArea() + Triangle(self.x1, self.y1, x, y, self.x3, self.y3).getArea() + Triangle(x, y, self.x2, self.y2, self.x3, self.y3).getArea() == self.getArea()


class Star:
    def __init__(self, xCenter: int, yCenter: int, nearLength: int, farLength: int, startAngle: float):
        self.triangles = [
            Triangle(
                int(math.cos((340 + i * 360 / 5 + startAngle) / 180 * math.pi) * nearLength) + xCenter,
                int(math.sin((340 + i * 360 / 5 + startAngle) / 180 * math.pi) * nearLength) + yCenter,
                int(math.cos((200 + i * 360 / 5 + startAngle) / 180 * math.pi) * nearLength) + xCenter,
                int(math.sin((200 + i * 360 / 5 + startAngle) / 180 * math.pi) * nearLength) + yCenter,
                int(math.cos((90 + i * 360 / 5 + startAngle) / 180 * math.pi) * farLength) + xCenter,
                int(math.sin((90 + i * 360 / 5 + startAngle) / 180 * math.pi) * farLength) + yCenter,
            ) for i in range(5)
        ]

    def isLocationIn(self, x: int, y: int):
        for triangle in self.triangles:
            if triangle.isLocationIn(x, y):
                return True

        return False


def getFlag(name: str):
    functionName = f"make{name.title().replace(' ', '')}Flag"

    if functionName in globals():
        return ImageTk.PhotoImage(image=eval(f"{functionName}()"), size=(600, 300))


finlandFlag = None


def initFlags(flags: list):
    for flag in flags:
        getFlag(flag)


def makeFinlandFlag():
    global finlandFlag
    if finlandFlag is None:
        flag = Image.new("RGB", (600, 300))

        for x in range(600):
            for y in range(300):
                if 165 < x <= 266 or 99 < y <= 200:
                    flag.putpixel((x, y), (0, 47, 108))
                else:
                    flag.putpixel((x, y), (255, 255, 255))

        finlandFlag = flag

    return finlandFlag


czechRepublicFlag = None


def makeCzechRepublicFlag():
    global czechRepublicFlag
    if czechRepublicFlag is None:
        flag = Image.new("RGB", (600, 300))

        blueTriangle = Triangle(0, 0, 223, 150, 0, 299)

        for x in range(600):
            for y in range(300):
                if blueTriangle.isLocationIn(x, y):
                    flag.putpixel((x, y), (17, 69, 126))
                elif y < 150:
                    flag.putpixel((x, y), (255, 255, 255))
                else:
                    flag.putpixel((x, y), (215, 20, 26))

        czechRepublicFlag = flag

    return czechRepublicFlag


togoFlag = None


def makeTogoFlag():
    global togoFlag
    if togoFlag is None:
        flag = Image.new("RGB", (600, 300))

        whiteStar = Star(90, 90, 20, 60, 180)

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

        togoFlag = flag

    return togoFlag
