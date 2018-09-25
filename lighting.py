# Lighting.py
# Contains a collection of preset lighting configurations for
# the interactive render script
from Sun import Sun
from Sky import Sky
from Vector3 import Vec3

def midDay(scene):
    sun = Sun(pos=Vec3(40, 100, 30))
    # orient sun
    sun.lookAt(Vec3(0, 0, 0))
    # Add sun to scene
    scene.addLight(sun)
    # Create sky
    sky = Sky()
    # Add sky to scene
    scene.addLight(sky)


def dusk(scene):
    sun = Sun(pos=Vec3(40, 20, 0), colour=Vec3(0.4, 0.2, 0.4))
    # orient sun
    sun.lookAt(Vec3(0, 0, 0))
    # Add sun to scene
    scene.addLight(sun)
    # Create sky
    sky = Sky()
    # Add sky to scene
    scene.addLight(sky)


def cloudy(scene):
    sky = Sky()
    # Add sky to scene
    scene.addLight(sky)


presets = {"midDay": midDay, "dusk": dusk, "cloudy": cloudy}
