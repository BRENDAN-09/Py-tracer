from Vector3 import Vec3
from Camera import Camera
from Scene import Scene
from Sun import Sun
from Sky import Sky
from timeit import default_timer as timer

# Create new scene
scene = Scene()
# Load Model and materials
scene.loadModel("blocks.obj", "blocks.mtl")
# Create Sun
sun = Sun(pos=Vec3(40, 100, 30))
sun.lookAt(Vec3(0, 0, 0))
scene.addLight(sun)
# Create sky
sky = Sky()
scene.addLight(sky)
# Create Camera
cam = Camera(Vec3(2, 10, 5), 512, 512, Fov=1, Samples=1)
cam.lookAt(Vec3(0, 0, 0))
# Render scene
ts = timer()
cam.render(scene)
print("Render time: {}".format(timer()-ts))
