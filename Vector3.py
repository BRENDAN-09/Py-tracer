# Vector3.py
from math import sqrt


class Vec3:
    def __init__(self, x_element, y_element, z_element):
        "initializes a vector class"
        self.x = x_element
        self.y = y_element
        self.z = z_element

    def __str__(self):
        "vector addition"
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)

    def __add__(self, a):
        "vector addition"
        return Vec3(self.x + a.x, self.y + a.y, self.z + a.z)

    def __sub__(self, a):
        "vector subtraction"
        return Vec3(self.x - a.x, self.y - a.y, self.z - a.z)

    def __mul__(self, a):
        "vector multiplication"
        return Vec3(self.x * a.x, self.y * a.y, self.z * a.z)

    def __truediv__(self, a):
        "vector division"
        return Vec3(self.x / a.x, self.y / a.y, self.z / a.z)

    def __xor__(self, a):
        "scaler multiplication"
        return Vec3(self.x * a, self.y * a, self.z * a)

    def clamp(self, a, b):  # B is Max
        "clamps the vector between a and b"
        self.x = min(b, max(a, self.x))
        self.y = min(b, max(a, self.y))
        self.z = min(b, max(a, self.z))


def Copy(a):
    "copies a vector"
    return Vec3(a.x, a.y, a.z)


def Dot(a, b):
    "computes the dot product of two vector"
    return a.x * b.x + a.y * b.y + a.z * b.z


def Cross(a, b):
    "computes the cross product of two vector"
    return Vec3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)


def Length(v):
    "computes the length of a vector"
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z)


def Normalize(v):
    return v ^ (1.0 / Length(v))
    # Return normal that is pointing on the side as the passed direction


def orient_normal(normal, direction):
    "flips a vector to match a direction"
    if Dot(normal, direction) < 0.0:
        return normal * -1.0  # flip normal
    else:
        return normal
