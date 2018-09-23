from Vector3 import Vec3
from Camera import Camera
from Scene import Scene
from Sun import Sun
from Sky import Sky
from timeit import default_timer as timer
from Octree import Braunch

samples = width = height = None

while True:
    try:
        samples = int(input("Number of samples: "))
    except:
        print("invalid answer. Must be integer")
        continue
    break

model = input("Model to render (.obj): ")
material = input("material file (.mtl): ")
while True:
    try:
        width = int(input("Width: "))
    except:
        print("invalid answer. Must be integer")
        continue
    break
while True:
    try:
        height = int(input("Height: "))
    except:
        print("invalid answer. Must be integer")
        continue
    break

# turn on tree
useTree = False
# Create new scene
scene = Scene()
# Load Model and materials
scene.loadModel(model, material)
# Create Sun
sun = Sun(pos=Vec3(40, 100, 30))
sun.lookAt(Vec3(0, 0, 0))
scene.addLight(sun)
# Create sky
sky = Sky()
scene.addLight(sky)
# Create Camera
cam = Camera(Vec3(-8, 5, 8), width, height, Fov=1.4, Samples=samples)
cam.lookAt(Vec3(0, 3, 0))
# Render scene
ts = timer()
if useTree:
    tree = Braunch()
    tree.fromScene(scene)
    cam.render(tree, "gu.png")
else:
    cam.render(scene, "gu.png")

print("Render time: {}".format(timer()-ts))
print("Intersections: ", scene.average)
