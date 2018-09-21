# Diffuse.py
# A vague and mis leading name for a script that features a variety of
# mathsy functions
from math import sqrt, cos, sin, pi
from random import random
from Vector3 import Vec3, Normalize, Cross

# return a point on the hemisphere from polar coordinates
def sampleHemisphere(u1, u2):
    # make r uniform over the sphere
    r = sqrt(u1)
    # scale theta to radians
    theta = 2 * pi * u2
    # calculate x and y
    x = r * cos(theta)
    y = r * sin(theta)

    return Vec3(x, y, sqrt(max(0, 1 - u1)))


def OrientedHemiDir(normal):
    p = sampleHemisphere(random(), random())  # random point on hemisphere
    return orthonormal(p, normal)  # make orthonormal to normal


def diskPoint(normal):
    theta = random() * 2 * pi  # theta in radians (0-2)
    mag = sqrt(random())  # sqrt makes the distribution uniform
    y = sin(theta) * mag
    x = cos(theta) * mag
    return orthonormal(Vec3(x, y, 0), normal)  # calculate x and


def orthonormal(p, normal):
    # create orthonormal basis around normal
    w = normal
    v = Cross(Vec3(0.00319, 0.0078, 1.0), w)  # jittered up
    v = Normalize(v)  # normalize
    u = Cross(v, w)

    hemi_dir = (u ^ p.x) + (v ^ p.y) + (w ^ p.z)  # linear projection
    return Normalize(hemi_dir)  # make direction
