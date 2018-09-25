# Sky.py
from Vector3 import Vec3, Normalize
from Diffuse import OrientedHemiDir
from Ray import Ray


class Sky:
    def __init__(self, colour=Vec3(0.6, 0.6, 0.55)):
        """initializes a sky class
        Optional parameters:
            colour: Vec3. The colour of the sun. Default Vec3(0.4, 0.4, 0.45)
        """
        self.colour = colour

    def randomPoint(self, normal):
        "returns a random point on the sky"
        return (OrientedHemiDir(normal) ^ 1000)

    def calcDirect(self, pos, nor, scene):
        """calculates the direct lighting from the sun on a point
        Parmeters:
            Pos: Vec3. The position of the point
            Normal: Vec3. The normal of the triangle
            scene: Scene. The scene that the triangle is in
        """
        liRay = Normalize(self.randomPoint(nor) - pos)
        return (self.colour ^ scene.worldShadow(Ray(orig=pos + (nor ^ 0.001), dir=liRay)))
