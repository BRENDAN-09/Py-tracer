# AABB.py
# Axis Aligned Bounding Box
from Vector3 import Vec3
from Ray import Ray
from Triangle import Triangle
import json


class AABB():
    def __init__(self, v1, v2):
        self.info = [v1, v2]


    def intersect(self, r):
        lo = -float("Inf")
        hi = float("Inf")

        for i in ["x", "y", "z"]:
            dimLo = (getattr(self.info[0], i) -
                     getattr(r.o, i)) / getattr(r.d, i)
            dimHi = (getattr(self.info[1], i) -
                     getattr(r.o, i)) / getattr(r.d, i)

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

    def subDivide(self):
        a = self.info[0]
        g = self.info[1]
        b = Vec3(g.x, a.y, a.z)
        c = Vec3(g.x, a.y, g.z)
        d = Vec3(a.x, a.y, g.z)
        e = Vec3(a.x, g.y, a.z)
        f = Vec3(b.x, g.y, b.z)
        h = Vec3(d.x, g.y, g.z)
        m = self.info[0] + ((self.info[1] - self.info[0]) ^ 0.5)
        boxes = []
        for i in [a, b, c, d, e, f, g, h]:
            boxes.append(AABB(i, m))
        return boxes


"""aabb = AABB(Vec3(1, 1, 1), Vec3(0, 0, 0))
r = Ray(orig=Vec3(2, 2, 2), dir=Vec3(-1, -1, -1))
i = aabb.containsPoint(Vec3(0.5, 1.2, 0.5))
t = Triangle(Vec3(0.1, 3, 0.1), Vec3(
    0.3, 0.3, 0.2), Vec3(0.8, 0.6, 0.2), "gre")
b = aabb.subDivide()
f = open("car.json", "w")
print(b)"""
