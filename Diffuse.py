# Diffuse.py
"""A vague and misleading name for a script that features a variety of
mathsy functions"""
from math import sqrt, cos, sin, pi
from random import random
from Vector3 import Vec3, Normalize, Cross


def sampleHemisphere(u1, u2):
    """Return a point on the hemisphere from polar coordinates
    u1: Float. the radius of the polar coordinats
    u2: Float. theta

    return: Vec3. point on hemisphere
    """
    # make r uniform over the sphere using the inverse itegral
    # of the distribution density
    r = sqrt(u1)
    # scale theta to radians
    theta = 2 * pi * u2
    # calculate x and y
    x = r * cos(theta)
    y = r * sin(theta)

    return Vec3(x, y, sqrt(max(0, 1 - u1)))


def OrientedHemiDir(normal):
    """
    Produces a random point on the hemisphere a around the normal
    normal: Vec3. The normal to be used
    return: Vec3. The random point on the hemisphere
    """
    p = sampleHemisphere(random(), random())  # random point on hemisphere
    return orthonormal(p, normal)  # make orthonormal to normal


def diskPoint(normal):
    """
    Returns a random point on a disk with a radius of 1
    normal: Vec3. The normal of the disk to be used
    return: Vec3. The random point
    """
    theta = random() * 2 * pi  # theta in radians (0-2)
    mag = sqrt(random())  # sqrt makes the distribution uniform
    y = sin(theta) * mag  # Generate x and y coords with some trig
    x = cos(theta) * mag
    return orthonormal(Vec3(x, y, 0), normal)  # rotate to match normal


def orthonormal(p, normal):
    """
    Translates a normalized vector to have its z axis aligned along
    a specific normal.

    p: Vec3 the vector to be translated
    normal: the normal for the vector to be translated around
    """
    # create orthonormal basis around normal
    w = normal
    v = Cross(Vec3(0.00319, 0.0078, 1.0), w)  # jittered up
    v = Normalize(v)  # normalize
    u = Cross(v, w)

    hemi_dir = (u ^ p.x) + (v ^ p.y) + (w ^ p.z)  # linear projection
    return Normalize(hemi_dir)  # make direction
