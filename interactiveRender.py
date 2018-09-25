from Vector3 import Vec3
from Camera import Camera
from Scene import Scene
from Sun import Sun
from Sky import Sky
from timeit import default_timer as timer
from Octree import Braunch
import lighting

samples = width = height = None

def inputInt(s):
    while True:
        try:
            proto = int(input(s))
        except:
            print("invalid answer. Must be integer")
            continue
        break
    return proto

samples = inputInt("Number of samples: ")
model = input("Model to render (.obj): ")
if ".obj" not in model:
    model += ".obj"
material = input("material file (.mtl): ")
if ".mtl" not in material:
    material += ".mtl"
width = inputInt("Output Width: ")
height = inputInt("Output Height: ")
while True:
    proto = input("lighting (" + str([i for i in lighting.presets]) + "): " )
    if proto in lighting.presets:
        break
preset = proto
output = input("output image name: ")
output += ".png"


# Create new scene
scene = Scene()
# Load Model and materials
scene.loadModel(model, material)
# Add lighting
lighting.presets[preset](scene)
# Create Camera
cam = Camera(Vec3(-8, 5, 8), width, height, Fov=1.4, Samples=samples)
cam.lookAt(Vec3(0, 3, 0))
# Render scene
ts = timer()
cam.render(scene, output)

print("Render time: {}".format(timer()-ts))
print("Intersections: ", scene.average)
