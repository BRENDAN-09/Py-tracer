from Octree import Braunch
from Scene import Scene
from Vector3 import Vec3
from timeit import default_timer as timer
from Sun import Sun
from Sky import Sky
from Camera import Camera

# Create new scene
scene = Scene()
# Load Model and materials
scene.loadModel("untitled.obj", "untitled.mtl")


sun = Sun(pos=Vec3(-20, 30, 30))
sun.lookAt(Vec3(0, 0, 0))
scene.addLight(sun)
sun.size = 3
# Create sky
sky = Sky(colour=Vec3(0.3, 0.2, 0.3))
scene.addLight(sky)
# Create Camera
cam = Camera(Vec3(-4, 3, -5), 256, 256, Fov=1, Samples=7)
cam.lookAt(Vec3(0, 0, 0))
tree = Braunch()
tree.fromScene(scene)
tree.display()
# Render scene
ts = timer()
cam.render(tree)
treeTime = timer() - ts
# print("Render time: {}".format(timer()-ts))
ts = timer()
cam.render(scene)
sceneTime = timer() - ts
print("Average intersections (scene): {}".format(scene.average))
print("Average intersections (tree):  {}".format(tree.average))
print("time  (tree): {}".format(treeTime))
print("time (scene): {}".format(sceneTime))
