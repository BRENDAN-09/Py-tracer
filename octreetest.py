from Octree import Braunch
from Scene import Scene
from AABB import AABB
from Vector3 import Vec3
from Ray import Ray
from timeit import default_timer as timer
from Diffuse import sampleHemisphere
from random import random
from Sun import Sun
from Sky import Sky
from Camera import Camera

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

tree = Braunch(AABB(Vec3(minx, miny , minz ),
                    Vec3(maxx , maxy , maxz )))
print(tree.bounds)
for t in scene.primitives:
    tree.grow(deepcopy(t))
r = Ray(orig=Vec3(0.5, 0.5, 1), dir=Vec3(0, -1, -1))
a = scene.worldIntersect(r)
b = tree.worldIntersect(r)
ts = timer()
"""for i in range(100000):
    d = []
    v = []
    for i in range(3):
        d.append(random()*7-3.5)
        v.append(random()*7-3.5)
    ray = Ray(orig=Vec3(*d), dir=Vec3(*v))
    tree.worldIntersect(ray)
print(timer()-ts)"""

sun = Sun(pos=Vec3(40, 100, 30))
sun.lookAt(Vec3(0, 0, 0))
scene.addLight(sun)
# Create sky
sky = Sky()
scene.addLight(sky)
# Create Camera
cam = Camera(Vec3(2, 10, 5), 512, 512, Fov=1, Samples=2)
cam.lookAt(Vec3(0, 0, 0))
tree.addMaterials(scene.materials)
tree.addLights(scene.lights)
print(len(tree.leaves))
print(len(tree.braunches))
print(tree.pri())
# Render scene
cam.render(tree)
print(timer()-ts)
