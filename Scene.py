# Scene.py
from Vector3 import Vec3, Copy
from Triangle import Triangle


class Scene:
    def __init__(self):
        "initializes a scene"
        self.primitives = []
        self.materials = {}
        self.lights = []
        self.average = 0

    def addPrimitive(self, prim):
        "adds a primitive to the scene"
        self.primitives.append(prim)

    def addLight(self, light):
        self.lights.append(light)

    def loadModel(self, path, mtl):
        """
        Loads a model from a obj and mtl file.
        Parmeters:
            path: String. The path to the obj file
            mtl: String. The path to the mtl file
        """
        mat = None
        if mtl is not None:
            for line in open(mtl):
                if "newmtl" in line:
                    # update current material
                    mat = line[7:].strip()
                elif line[0:2] == "Kd":
                    # add material colour
                    self.materials[mat] = (
                        Vec3(*(map(float, line[3:].strip().split()))))
        verts = []
        for line in open(path):
            # If line is a vertex
            if line[0] == "v":
                # Add vertex
                verts.append(
                    Vec3(*(map(float, line[1:].strip().split(" ")))))
            # If line is a face
            if line[0] == "f":
                # add face
                a = line[1:].strip().split(" ")
                self.addPrimitive(
                    Triangle(*[Copy(verts[int(i) - 1]) for i in a], mat))
            # if line is a material declaration
            if "usemtl" in line:
                mat = line[7:].strip()  # Update material

    def worldIntersect(self, ray):
        """
        intersects the ray with the octree.
        Parameters:
            r: Ray. The ray to intersect
        return: Tuple (Bool hit, Float distance, Vec3 normal)
        """
        # the closest intersection so far
        close = (False, float("inf"), Vec3(0, 0, 0))
        index = -1
        for i in range(len(self.primitives)):
            intersection = self.primitives[i].intersect(ray)
            self.average += 1
            # if there's a new closest intersection update index and close
            if intersection[0] and 0 < intersection[1] < close[1]:
                close = intersection
                index = i
        return {"t": close, "index": self.primitives[index]}

    # return 0 if there is an intersection, 1 otherwise
    def worldShadow(self, ray):
        """
        intersects the ray with the octree.
        Parameters:
            r: Ray. The ray to intersect
        return: Int. 0 if intersection exists otherwise 1.
        """
        # iterate over the primitives
        for i in self.primitives:
            sec = i.intersect(ray)
            if sec[0] and 0 < sec[1]:  # make sure the intersection is positive
                return 0
        return 1
