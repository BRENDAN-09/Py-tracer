from math import sqrt, sin, cos, pi
from random import random
TWO_PI = 6.282


class Vector3D:
    # Initializer
    def __init__(self, x_element, y_element, z_element):
        self.x = x_element
        self.y = y_element
        self.z = z_element

    # Operator Overloading
    def __str__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)

    def __sub__(self, v):
        return Vector3D(self.x - v.x, self.y - v.y, self.z - v.z)

    def __add__(self, v):
        return Vector3D(self.x + v.x, self.y + v.y, self.z + v.z)

    def __mul__(self, s):
        return Vector3D(self.x * s, self.y * s, self.z * s)

    def __truediv__(self, s):
        return Vector3D(self.x / s, self.y / s, self.z / s)


def Dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z
# Return perpendicular vector


def Cross(a, b):
    return Vector3D(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)
# Return length of vector


def Length(v):
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
# Return normalized vector (unit vector)


def Normalize(v):
    return v * (1.0 / Length(v))
# Return normal that is pointing on the side as the passed direction

def sampleHemisphere(u1, u2):
    r = sqrt(u1)
    theta = 2 * pi * u2

    x = r * cos(theta)
    y = r * sin(theta)

    return Vector3D(x, y, sqrt(max(0, 1 - u1)))


def OrientedHemiDir(u1, u2, normal):
    p = sampleHemisphere(u1, u2)  # random point on hemisphere

    # create orthonormal basis around normal
    w = normal
    v = Cross(Vector3D(0.00319, 0.0078, 1.0), w)  # jittered up
    v = Normalize(v)  # normalize
    u = Cross(v, w)

    hemi_dir = (u * p.x) + (v * p.y) + (w * p.z)  # linear projection
    return Normalize(hemi_dir)


n = Normalize(Vector3D(-1, -1, -1))
for i in range(10):
    s = OrientedHemiDir(random(), random(), n)
    print(Dot(s, n))
