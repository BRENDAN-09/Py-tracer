# RenderIt.py
"An example for how to use this program to render"
from Vector3 import Vec3
from Camera import Camera
from Scene import Scene
from Sun import Sun
from Sky import Sky
from Octree import Braunch
from timeit import default_timer as timer
# Create new scene
scene = Scene()
# Load Model and materials
scene.loadModel("models/planet.obj", "models/planet.mtl")
# Create Sun
sun = Sun(pos=Vec3(40, 100, 30))
# orient sun
sun.lookAt(Vec3(0, 0, 0))
# Add sun to scene
scene.addLight(sun)
# Create sky
sky = Sky()
# Add sky to scene
scene.addLight(sky)
# Create Camera (pos, width height)
cam = Camera(Vec3(3.5, 4, 0), int(400), int(200), Fov=1.4, Samples=2)
# Orient camera
cam.lookAt(Vec3(0, 3, 0))
# Render scene
ts = timer()
cam.render(scene, "flower.png")
print("Time elapsed: {}s".format(timer()-ts))
"""
To render a scene from an octree do:
tree = Braunch()
tree.fromScene(scene)
cam.render(tree, "flower.png")
"""
