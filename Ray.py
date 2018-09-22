# Ray.py
from Vector3 import Vec3, Normalize


class Ray:
    "Represents a ray with a origin and direction"
    def __init__(self, orig=Vec3(0, 0, 0), dir=Vec3(0, 0, 0)):
        """
        Initializes the ray.
        Optional parameters:
            orig: Vec3. The origin of the ray.
            dir: Vec3. The direction of the ray.
        """
        self.o = orig
        self.d = Normalize(dir)
