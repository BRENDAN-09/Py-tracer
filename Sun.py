# Sun.py
from Vector3 import Vec3, Normalize, Dot
from Diffuse import diskPoint
from Ray import Ray


class Sun:
    def __init__(self, size=2, normal=Vec3(0, 0, 1), pos=Vec3(1, 0, 0), colour=Vec3(0.97, 0.97, 0.72)):
        self.size = size
        self.normal = normal
        self.pos = pos
        self.colour = colour

    def lookAt(self, pos):
        self.normal = Normalize(pos - (self.pos))

    def randomPoint(self):
        return self.pos + (diskPoint(self.normal) ^ self.size)

    def calcDirect(self, pos, nor, scene):
        liRay = Normalize(self.randomPoint() - pos)
        factor = Dot(liRay, nor)
        return (self.colour ^ scene.worldShadow(  # Sun light
                Ray(orig=pos + (nor ^ 0.000001), dir=liRay)) ^ factor)
