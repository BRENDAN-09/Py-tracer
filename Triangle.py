# Triangle.py
"""
This file contains the triangle class as well as a function Copytri() which
copies triangles.
"""
from Vector3 import Dot, Cross, Normalize, Vec3


class Triangle():
    "Represents a triangle in 3d space"
    def __init__(self, v0, v1, v2, mat):
        """Creates a triangle class for intersections
        v0: Vec3 first vertex
        v1: Vec3 second vertex
        v2: Vec3 third vertex
        mat: String Material of the triangle
        return: None
        """
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.mat = mat  # Material, not matrix
        self.normal = self.computeNormal()  # save triangle normal

    # Returns the triangle as a string for easy printing
    def __str__(self):
        "converts the triangle to a string"
        return "({0}, {1}, {2})".format(self.v0, self.v1, self.v2)

    def computeNormal(self):
        "gets the normal of the triangle"
        v0v1 = self.v1 - self.v0
        v0v2 = self.v2 - self.v0
        # A cross product of 2 vectors is perpendicular to both vectors.
        # A cross product of 2 of the triangle's edges is equivalent to the
        # Normal of a triangle
        return Normalize(Cross(v0v1, v0v2))

    def intersect(self, ray):
        """Intersects a ray with a Triangle
        ray: Ray the ray to be intersected
        return: Tuple (Bool hit, Float distance, Vec3 normal)
        """
        # Miss tuple
        miss = (False, 0, Vec3(0, 0, 0))
        normal = Vec3(0, 0, 0)
        v0 = self.v0
        v1 = self.v1
        v2 = self.v2
        # edges of the triangle
        v0v1 = v1 - v0
        v0v2 = v2 - v0
        # Determinant of a 3*3 matrix using triple scaler product
        pvec = Cross(ray.d, v0v2)
        det = Dot(v0v1, pvec)

        if det < 0.000001:
            return miss

        invDet = 1.0 / det
        tvec = ray.o - v0
        u = Dot(tvec, pvec) * invDet
        # make sure the barycentric coordinates are in the triangle
        if u < 0 or u > 1:
            return miss

        qvec = Cross(tvec, v0v1)
        v = Dot(ray.d, qvec) * invDet

        # make sure the barycentric coordinates are in the triangle
        if v < 0 or u + v > 1:
            return miss

        return (True, Dot(v0v2, qvec) * invDet, self.normal)


def Copytri(t):
    """Copies a triangle)

    :param triangle: Triangle. the triangle to be copied
    :return: Triangle. A copy of the input
    """
    return Triangle(t.v0, t.v1, t.v2, t.mat)
