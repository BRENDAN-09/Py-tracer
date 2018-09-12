# Octree.py
from Vector3 import Vec3
from Triangle import Triangle
from AABB import AABB

class Braunch():
    def __init__(self, bounds):
        self.leaves = []
        self.braunches = []
        self.bounds = bounds
        self.newGrowth = []

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

tree = Braunch(AABB(Vec3(0, 0, 0), Vec3(5, 5, 5)))
t = Triangle(Vec3(0.1, 0.1, 0.1), Vec3(0.3, 0.3, 0.2), Vec3(0.8, 0.6, 0.2), "gre")
tree.grow(t)
