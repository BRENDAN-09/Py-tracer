# Sun.py
from Vector3 import Vec3, Normalize, Dot
from Diffuse import diskPoint
from Ray import Ray


class Sun:
    def __init__(self, size=2, normal=Vec3(0, 0, 1), pos=Vec3(1, 0, 0), colour=Vec3(0.97, 0.97, 0.72)):
        """
        Initializes a sun class
        Optional Parmeters:
            size: Float. The size of the sun. Default 2
            normal: Vec3. The direction the sun's facing. Default Vec3(0, 0, 1)
            pos: Vec3. The position of the sun. Default Vec3(1, 0, 0)
            colour: Vec3. The colour of the sun.
                Default colour=Vec3(0.97, 0.97, 0.72)
        """
        self.size = size
        self.normal = normal
        self.pos = pos
        self.colour = colour

    def lookAt(self, pos):
        "rotates the sun to look at pos"
        self.normal = Normalize(pos - (self.pos))

    def randomPoint(self):
        "returns a random point on the disk"
        return self.pos + (diskPoint(self.normal) ^ self.size)

    def calcDirect(self, pos, nor, scene):
        """calculates the direct lighting from the sun on a point
        Parmeters:
            Pos: Vec3. The position of the point
            Normal: Vec3. The normal of the triangle
            scene: Scene. The scene that the triangle is in
        """
        liRay = Normalize(self.randomPoint() - pos)  # Create shadow ray
        factor = Dot(liRay, nor)  # Calculate factor
        return (self.colour ^ scene.worldShadow(  # Sun light
                Ray(orig=pos + (nor ^ 0.000001), dir=liRay)) ^ factor)
