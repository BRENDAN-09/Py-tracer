# Octree.py
from Vector3 import Vec3
from Triangle import Triangle
from AABB import AABB


class Braunch():
    def __init__(self, bounds):
        self.leaves = []
        self.braunches = []
        self.bounds = bounds

    def grow(self, triangle):
        braunches = [Braunch(i) for i in self.bounds.subDivide()]
        for b in braunches:
            print(b.bounds.containsTri(triangle))
            if b.bounds.containsTri(triangle):
                print(b.bounds)
                b.grow(triangle)
                break
        else:
            self.leaves.append(triangle)
        self.braunches.append(braunches)

    def intersect(self, r):
        miss = (False, float("inf"), Vec3(0, 0, 0))
        queue = [self]
        for i in queue:
            if i.bounds.intersect(r):
                # Check leaves
                intersect = self.intersectLeaves(i.leaves, r)
                if intersect[0] and 0 < intersect[1] < miss[1]:
                    miss = intersect
                # Check braunches
                queue += i.braunches

    def intersectLeaves(self, leaves, ray):
        close = (False, float("inf"), Vec3(0, 0, 0))
        index = -1
        for i in range(len(leaves)):
            intersection = leaves[i].intersect(ray)
            if intersection[0] and 0 < intersection[1] < close[1]:
                close = intersection
                index = i
        return close


"""tree = Braunch(AABB(Vec3(0, 0, 0), Vec3(5, 5, 5)))
t = Triangle(Vec3(0.1, 0.1, 0.1), Vec3(0.3, 0.3, 0.2), Vec3(0.8, 0.6, 0.2), "gre")
tree.grow(t)"""
