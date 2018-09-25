from Vector3 import Vec3
from Camera import Camera
from Scene import Scene
from Sun import Sun
from Sky import Sky
from Octree import Braunch

# Create new scene
scene = Scene()
# Load Model and materials
scene.loadModel("models/flower.obj", "models/flower.mtl")
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
cam = Camera(Vec3(0, 5, 8), int(1260), int(2240), Fov=1.4, Samples=100)
# Orient camera
cam.lookAt(Vec3(0, 3, 0))
# Render scene
cam.render(scene, "flower.png")
"""
To render a scene from an octree do:
tree = Braunch()
tree.fromScene(scene)
cam.render(tree, "flower.png")
"""
