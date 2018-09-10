from math import sqrt, cos, sin, pi
from random import random
from Vector3 import Vec3, Normalize, Cross


def sampleHemisphere(u1, u2):
    r = sqrt(u1)
    theta = 2 * pi * u2

    x = r * cos(theta)
    y = r * sin(theta)

    return Vec3(x, y, sqrt(max(0, 1 - u1)))


def OrientedHemiDir(normal):
    p = sampleHemisphere(random(), random())  # random point on hemisphere
    return orthonormal(p, normal)


def diskPoint(normal):
    theta = random() * 2 * pi
    mag = sqrt(random())  # sqrt makes the distribution uniform
    y = sin(theta) * mag
    x = cos(theta) * mag
    return orthonormal(Vec3(x, y, 0), normal)


def orthonormal(p, normal):
    # create orthonormal basis around normal
    w = normal
    v = Cross(Vec3(0.00319, 0.0078, 1.0), w)  # jittered up
    v = Normalize(v)  # normalize
    u = Cross(v, w)

    hemi_dir = (u ^ p.x) + (v ^ p.y) + (w ^ p.z)  # linear projection
    return Normalize(hemi_dir)
