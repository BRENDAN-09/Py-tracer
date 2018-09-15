# Octree.py
from Vector3 import Vec3, Dot
from Triangle import Copytri


class Braunch():
    def __init__(self, bounds):
        self.leaves = []
        self.braunches = []
        self.materials = {}
        self.bounds = bounds
        self.lights = []
        self.average = 0
        self.time = 0

    def grow(self, triangle):
        activeBox = self
        itFits = True
        while itFits:
            if len(activeBox.braunches) == 0:
                activeBox.braunches = [
                    Braunch(i) for i in activeBox.bounds.subDivide()]
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
            total += len(i.leaves)
        return total

    def worldIntersect(self, r):
        miss = (False, float("inf"), Vec3(0, 0, 0))
        queue = [self]
        index = None
        for i in queue:
            if i.bounds.intersect(r) < 1000:
                # Check leaves
                intersect, indet = self.intersectLeaves(i.leaves, r)
                self.average += len(i.leaves)
                self.time += 1
                if intersect[0] and 0 < intersect[1] < miss[1]:
                    miss = intersect
                    index = indet
                # Check braunches
                queue += i.braunches
        # print(total)
        return {"t": miss, "index": index}

    def worldShadow(self, r):
        queue = [self]
        for i in queue:
            if i.bounds.intersect(r) < 1000:
                # Check leaves
                intersect, indet = self.intersectLeaves(i.leaves, r)
                self.average += len(i.leaves)
                self.time += 1
                if intersect[0] and 0 < intersect[1] < 100000:
                    return 0
                # Check braunches
                queue += i.braunches
        # print(total)
        return 1

    def addMaterials(self, m):
        self.materials = m

    def addLights(self, l):
        self.lights = l

    # prints a textual representation of the tree
    def display(self):
        queue = [[self, 0]]
        q = 0
        prevdepth = 0
        while len(queue) > 0:
            active = queue.pop()
            q += len(active[0].leaves)
            if not prevdepth == active[1]:
                print(str(active[1]) + "    " * active[1] + str(q))
                q = 0
            prevdepth = active[1]
            queue += [[i, active[1]+1] for i in active[0].braunches]

    def intersectLeaves(self, leaves, ray):
        close = (False, float("inf"), Vec3(0, 0, 0))
        indie = None
        for i in leaves:
            intersection = i.intersect(ray)
            if intersection[0] and 0 < intersection[1] < close[1]:
                close = intersection
                indie = i
        return close, indie
