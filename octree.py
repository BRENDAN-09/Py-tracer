# Octree.py
from Vector3 import Vec3
from Triangle import Triangle, Copytri
from AABB import AABB
from Ray import Ray
from copy import deepcopy


class Braunch():
    def __init__(self, bounds):
        self.leaves = []
        self.braunches = []
        self.materials = {}
        self.bounds = bounds
        self.lights = []

    # WRONG!!!! makes no sense
    def grow(self, triangle):
        activeBox = self
        possibilities = None
        itFits = True
        t = 0
        while itFits:
            if len(activeBox.braunches) == 0:
                activeBox.braunches = [Braunch(i) for i in activeBox.bounds.subDivide()]
            for i in activeBox.braunches:
                # print(i.bounds, triangle)
                if i.bounds.containsTri(triangle):
                    activeBox = i
                    break
            else:
                activeBox.leaves.append(triangle)
                itFits = False
    def pri(self):
        queue = [self]
        total = 0
        for i in queue:
            queue += i.braunches
            total+=len(i.leaves)
        return total

    def worldIntersect(self, r):
        miss = (False, float("inf"), Vec3(0, 0, 0))
        queue = [self]
        index = None
        # total = 0
        for i in queue:
            if i.bounds.intersect(r)<1000:
                # Check leaves
                intersect, indet = self.intersectLeaves(i.leaves, r)
                # total += len(i.leaves)
                if intersect[0] and 0 < intersect[1] < miss[1]:
                    miss = intersect
                    index = indet
                # Check braunches
                queue += i.braunches
        # print(total)
        return {"t": miss, "index": index}

    def worldShadow(self, r):
        return 0 if self.worldIntersect(r)["t"][0] else 1

    def addMaterials(self, m):
        self.materials = m

    def addLights(self, l):
        self.lights = l

    def intersectLeaves(self, leaves, ray):
        close = (False, float("inf"), Vec3(0, 0, 0))
        indie = None
        for i in range(len(leaves)):
            intersection = leaves[i].intersect(ray)
            if intersection[0] and 0 < intersection[1] < close[1]:
                close = intersection
                indie = Copytri(leaves[i])
        return close, indie
