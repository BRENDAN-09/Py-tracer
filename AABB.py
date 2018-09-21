# AABB.py
# Axis Aligned Bounding Box
from Vector3 import Vec3
from Ray import Ray
from Triangle import Triangle
import json


class AABB():
    def __init__(self, v1, v2):
        self.info = [v1, v2]

    def __str__(self):
        return "" + str(self.info[0]) + ", " + str(self.info[1])

    def intersect(self, r):
        lo = -float("Inf")
        hi = float("Inf")

        for i in ["x", "y", "z"]:
            divisor = getattr(r.d, i)
            # Avoid dividing by zero
            if divisor == 0:
                divisor += 0.0000000001
            dimLo = (self.info[0].__dict__.get(i) -
                     r.o.__dict__.get(i)) / divisor
            dimHi = (getattr(self.info[1], i) -
                     getattr(r.o, i)) / divisor

            # Swap so that dimHi > dimLo
            if dimLo > dimHi:
                dimLo, dimHi = dimHi, dimLo
            # chech the ray hasn't missed
            if dimHi < lo or dimLo > hi:
                return float("Inf")
            # Update dimLo and dimHi
            if dimLo > lo:
                lo = dimLo

            if dimHi < hi:
                hi = dimHi

        return float("Inf") if lo > hi else lo

    def containsPoint(self, p):
        # iterate over dimensions
        for i in ["x", "y", "z"]:
            # iterate through the dimensions
            # get dimensional range
            tmin = getattr(self.info[0], i)
            tmax = getattr(self.info[1], i)
            q = getattr(p, i)
            # check if p is in dimensional range
            if not((tmin <= q <= tmax) or (tmax <= q <= tmin)):
                return False
        return True

    def containsTri(self, t):
        # iterate through points
        for i in ["v0", "v1", "v2"]:
            # check if point is in box
            p = self.containsPoint(getattr(t, i))
            if not p:
                return False
        # only if all three points are in the box is the triangle in the box
        return True

    def subDivide(self):
        # A-H represent the 8 corners of the box
        # M is the midpoint of the box
        a = self.info[0]
        g = self.info[1]
        b = Vec3(g.x, a.y, a.z)
        c = Vec3(g.x, a.y, g.z)
        d = Vec3(a.x, a.y, g.z)
        e = Vec3(a.x, g.y, a.z)
        f = Vec3(b.x, g.y, b.z)
        h = Vec3(d.x, g.y, g.z)
        # Calculate midpoint
        m = self.info[0] + ((self.info[1] - self.info[0]) ^ 0.5)
        boxes = []
        # Construct all 8 boxes
        for i in [a, b, c, d, e, f, g, h]:
            boxes.append(AABB(i, m))
        return boxes
