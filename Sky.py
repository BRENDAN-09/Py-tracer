# Sky.py
from Vector3 import Vec3, Normalize
from Diffuse import OrientedHemiDir
from Ray import Ray


class Sky:
    def __init__(self, colour=Vec3(0.4, 0.4, 0.45)):
        self.colour = colour

    def randomPoint(self, normal):
        return (OrientedHemiDir(normal) ^ 1000)

    def calcDirect(self, pos, nor, scene):
        liRay = Normalize(self.randomPoint(nor) - pos)
        return (self.colour ^ scene.worldShadow(Ray(orig=pos + (nor ^ 0.001), dir=liRay)))
