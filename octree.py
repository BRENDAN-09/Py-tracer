# Octree.py
# Contains the octree class
from Vector3 import Vec3, Dot
from Triangle import Copytri
from AABB import AABB


class Braunch():
    def __init__(self, b=AABB(Vec3(0, 0, 0), Vec3(0, 0, 0))):
        """
        Initializes a Braunch Class
        """
        self.leaves = []
        self.braunches = []
        self.materials = {}
        self.bounds = b
        self.lights = []
        self.average = 0
        self.time = 0

    def fromScene(self, scene):
        """
        Constructs an octree from a scene
        Parameters:
            Scene: Scene. The scene to construct an octree from.
        """
        # Calculate the bounding box of the scene
        minx = miny = minz = +10000
        maxx = maxy = maxz = -10000
        for i in scene.primitives:
            minx = min(min(i.v0.x, i.v1.x, i.v2.x), minx)
            miny = min(min(i.v0.y, i.v1.y, i.v2.y), miny)
            minz = min(min(i.v0.z, i.v1.z, i.v2.z), minz)
            maxx = max(max(i.v0.x, i.v1.x, i.v2.x), maxx)
            maxy = max(max(i.v0.y, i.v1.y, i.v2.y), maxy)
            maxz = max(max(i.v0.z, i.v1.z, i.v2.z), maxz)
        self.bounds = AABB(Vec3(minx, miny, minz),
                           Vec3(maxx, maxy, maxz))
        for t in scene.primitives:
            self.grow((t))
        self.addMaterials(scene.materials)
        self.addLights(scene.lights)

    def grow(self, triangle):
        """
        Adds a triangle to the octree.
        Parameters:
            triangle: Triangle. The triangle to add.
        """
        activeBox = self
        itFits = True
        while itFits:
            for i in activeBox.braunches:
                # print(i.bounds, triangle)
                if i.bounds.containsTri(triangle):
                    activeBox = i
                    break
            else:
                if len(activeBox.braunches) < 8:
                    braunches = [
                        Braunch(b=i) for i in activeBox.bounds.subDivide() if i.containsTri(triangle)]
                    if len(braunches) > 0:
                        activeBox.braunches += braunches
                        activeBox = braunches[0]
                    else:
                        activeBox.leaves.append(triangle)
                        itFits = False
                else:
                    activeBox.leaves.append(triangle)
                    itFits = False

    def pri(self):
        "counts the number of leaves (not important)"
        queue = [self]
        total = 0
        for i in queue:
            queue += i.braunches
            total += len(i.leaves)
        return total

    def collapse(self):
        "culls a braunch (not important)"
        queue = [self]
        while len(queue) > 0:
            i = queue.pop()
            # Update queue
            queue += i.braunches
            self.leaves += i.leaves
        self.leaves = []

    def worldIntersect(self, r):
        """
        intersects the ray with the octree.
        Parameters:
            r: Ray. The ray to intersect
        return: Tuple (Bool hit, Float distance, Vec3 normal)
        """
        miss = (False, float("inf"), Vec3(0, 0, 0))
        # Breadth first search
        queue = [self]
        index = None
        for i in queue:
            if i.bounds.intersect(r) < 1000:
                # Check leaves
                intersect, indet = self.intersectLeaves(i.leaves, r)
                if intersect[0] and 0 < intersect[1] < miss[1]:
                    miss = intersect
                    index = indet
                # Check braunches
                queue += i.braunches
        # print(total)
        return {"t": miss, "index": index}

    def worldShadow(self, r):
        """
        intersects the ray with the octree.
        Parameters:
            r: Ray. The ray to intersect
        return: Int. 0 if intersection exists otherwise 1.
        """
        queue = [self]
        for i in queue:
            if i.bounds.intersect(r) < 1000:
                # Check leaves
                intersect, indet = self.intersectLeaves(i.leaves, r)
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
            q = active[0]
            print(str(active[1]) + "    " * active[1] +
                  "Branches: {}, Leaves {}".format(len(q.braunches), len(q.leaves)))
            queue += [[i, active[1] + 1] for i in active[0].braunches]

    def intersectLeaves(self, leaves, ray):
        close = (False, float("inf"), Vec3(0, 0, 0))
        indie = None
        self.average += len(leaves)
        for i in leaves:
            intersection = i.intersect(ray)
            if intersection[0] and 0 < intersection[1] < close[1]:
                close = intersection
                indie = i
        return close, indie
