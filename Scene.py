# Scene.py
from Vector3 import Vec3, Copy
from Triangle import Triangle


class Scene:
    def __init__(self):
        self.primitives = []
        self.materials = {}
        self.lights = []

    def addPrimitive(self, prim):
        self.primitives.append(prim)

    def addLight(self, light):
        self.lights.append(light)

    def loadModel(self, path, mtl):
        mat = None
        if mtl is not None:
            for line in open(mtl):
                if "newmtl" in line:
                    mat = line[7:].strip()
                elif line[0:2] == "Kd":
                    self.materials[mat] = (
                        Vec3(*(map(float, line[3:].strip().split()))))
        verts = []
        for line in open(path):
            if line[0] == "v":
                verts.append(
                    Vec3(*(map(float, line[1:].strip().split(" ")))))
            if line[0] == "f":
                a = line[1:].strip().split(" ")
                self.addPrimitive(
                    Triangle(*[Copy(verts[int(i) - 1]) for i in a], mat))
            if "usemtl" in line:
                mat = line[7:].strip()

    def worldIntersect(self, ray):
        close = (False, float("inf"), Vec3(0, 0, 0))
        index = -1
        for i in range(len(self.primitives)):
            intersection = self.primitives[i].intersect(ray)
            if intersection[0] and 0 < intersection[1] < close[1]:
                close = intersection
                index = i
        return {"t": close, "index": self.primitives[index]}

    # return 0 if there is an intersection, 1 otherwise
    def worldShadow(self, ray):
        for i in self.primitives:
            sec = i.intersect(ray)
            if sec[0] and 0 < sec[1]:  # make sure the intersection is positive
                return 0
        return 1
