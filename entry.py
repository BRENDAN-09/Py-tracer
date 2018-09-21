from Vector3 import Vec3
from Camera import Camera
from Scene import Scene
from Sun import Sun
from Sky import Sky
from timeit import default_timer as timer
from Octree import Braunch

# turn on tree
useTree = False
# Create new scene
scene = Scene()
# Load Model and materials
scene.loadModel("models/monkey.obj", "models/monkey.mtl")
# Create Sun
sun = Sun(pos=Vec3(40, 20, 30), colour=Vec3(0.74, 0.62, 0.69))
sun.lookAt(Vec3(0, 0, 0))
scene.addLight(sun)
sun.size = 5
# Create sky
sky = Sky()
scene.addLight(sky)
# Create Camera
cam = Camera(Vec3(2, 1, 6), int(128), int(128), Fov=1, Samples=40)
cam.lookAt(Vec3(-2, 0, 0))
# Render scene
ts = timer()
if useTree:
    tree = Braunch()
    tree.fromScene(scene)
    cam.render(tree)
else:
    cam.render(scene)
# print 
print("Render time: {}".format(timer()-ts))
print(scene.average)
