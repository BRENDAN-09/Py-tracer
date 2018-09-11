# AABB.py
# Axis Aligned Bounding Box
from Vector3 import Vec3
from Ray import Ray
from Triangle import Triangle


class AABB():
    def __init__(self, v1, v2):
        self.info = [v1, v2]

    def intersect(self, r):
        lo = -float("Inf")
        hi = float("Inf")

        for i in ["x", "y", "z"]:
            dimLo = (getattr(self.info[0], i) - getattr(r.o, i)) / getattr(r.d, i)
            dimHi = (getattr(self.info[1], i) - getattr(r.o, i)) / getattr(r.d, i)

            # Swap so that dimHi > dimLo
            if dimLo > dimHi:
                dimLo, dimHi = dimHi, dimLo

            if dimHi < lo or dimLo > hi:
                return float("Inf")

            if dimLo > lo:
                lo = dimLo

            if dimHi < hi:
                hi = dimHi

        return float("Inf") if lo > hi else lo

    def containsPoint(self, p):
        for i in ["x", "y", "z"]:
            tmin = getattr(self.info[0], i)
            tmax = getattr(self.info[1], i)
            q = getattr(p, i)
            if not((tmin <= q <= tmax) or (tmax <= q <= tmin)):
                return False
        return True

    def containsTri(self, t):
        for i in ["v0", "v1", "v2"]:
            p = self.containsPoint(getattr(t, i))
            if not p:
                return False
        return True


aabb = AABB(Vec3(0, 0, 0), Vec3(1, 1, 1))
r = Ray(orig=Vec3(200, 2, 2), dir=Vec3(1, 1, 1))
i = aabb.containsPoint(Vec3(0.5, 1.2, 0.5))
t = Triangle(Vec3(0.1, 3, 0.1), Vec3(0.3, 0.3, 0.2), Vec3(0.8, 0.6, 0.2), "gre")
print(aabb.containsTri(t))
