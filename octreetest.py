from Octree import Braunch
from Scene import Scene
from AABB import AABB
from Vector3 import Vec3
from Ray import Ray
from timeit import default_timer as timer
from Sun import Sun
from Sky import Sky
from Camera import Camera

# Create new scene
scene = Scene()
# Load Model and materials
scene.loadModel("blocks.obj", "blocks.mtl")
# Create new Octree
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

tree = Braunch(AABB(Vec3(minx, miny , minz ),
                    Vec3(maxx , maxy , maxz )))

for t in scene.primitives:
    tree.grow((t))


sun = Sun(pos=Vec3(40, 100, 30))
sun.lookAt(Vec3(0, 0, 0))
scene.addLight(sun)
# Create sky
sky = Sky()
scene.addLight(sky)
# Create Camera
cam = Camera(Vec3(-2, 3, -3), 128, 128, Fov=1, Samples=1)
cam.lookAt(Vec3(0, 0, 0))
tree.addMaterials(scene.materials)
tree.addLights(scene.lights)
print(len(tree.leaves))
print(len(tree.braunches))
print(tree.pri())
tree.display()
# Render scene
ts = timer()
cam.render(tree)
print("Render time: {}".format(timer()-ts))
print("Average intersections: {}".format(tree.average/tree.time))
