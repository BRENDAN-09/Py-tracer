# Ray.py
from Vector3 import Vec3, Normalize


class Ray:
    def __init__(self, orig=Vec3(0, 0, 0), dir=Vec3(0, 0, 0)):
        self.o = orig
        self.d = Normalize(dir)
