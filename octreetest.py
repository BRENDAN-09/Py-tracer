from Octree import Braunch
from Scene import Scene
from AABB import AABB
from Vector3 import Vec3
from Ray import Ray
from timeit import default_timer as timer
from Diffuse import sampleHemisphere
from random import random

# Create new scene
scene = Scene()
# Load Model and materials
scene.loadModel("untitled.obj", "untitled.mtl")
# Create new Octree
minx = miny = minz = +10000
maxx = maxy = maxz = -10000
for i in scene.primitives:
    minx = min(min(i.v0.x, i.v1.x, i.v2.x), minx)
    miny = min(min(i.v0.y, i.v1.y, i.v2.y), miny)
    minz = min(min(i.v0.z, i.v1.z, i.v2.z), minz)
    maxx = max(max(i.v0.x, i.v1.x, i.v2.x), maxx)
    maxy = max(max(i.v0.y, i.v1.y, i.v2.y), maxy)
    maxz = max(max(i.v0.z, i.v1.z, i.v2.z), maxz)

tree = Braunch(AABB(Vec3(minx - 1, miny - 1, minz - 1),
                    Vec3(maxx + 1, maxy + 1, maxz + 1)))
print(tree.bounds)
for t in scene.primitives:
    tree.grow(t)
r = Ray(orig=Vec3(0.5, 0.5, 1), dir=Vec3(0, -1, -1))
a = scene.worldIntersect(r)
b = tree.worldIntersect(r)
ts = timer()
for i in range(100000):
    d = []
    v = []
    for i in range(3):
        d.append(random()*7-3.5)
        v.append(random()*7-3.5)
    ray = Ray(orig=Vec3(*d), dir=Vec3(*v))
    tree.worldIntersect(ray)
print(timer()-ts)
