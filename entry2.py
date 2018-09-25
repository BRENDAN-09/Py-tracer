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
scene.loadModel("models/pyramid.obj", "models/pyramid.mtl")
# Create Sun
sun = Sun(pos=Vec3(40, 100, 30))
sun.lookAt(Vec3(0, 0, 0))
scene.addLight(sun)
# Create sky
sky = Sky()
scene.addLight(sky)
# Create Camera
cam = Camera(Vec3(8, 4, 8), int(2000), int(2000), Fov=1.4, Samples=200)
cam.lookAt(Vec3(0, 3, 0))
# Render scene
ts = timer()
if useTree:
    tree = Braunch()
    tree.fromScene(scene)
    cam.render(tree, "pyramid.png")
else:
    cam.render(scene, "pyramid.png")
"""w = 100
h = 200
for x in range(0,100,10):
    print(x)"""

print("Render time: {}".format(timer()-ts))
print(scene.average)
