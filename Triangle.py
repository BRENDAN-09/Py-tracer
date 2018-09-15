# Triangle.py
from Vector3 import Dot, Cross, Normalize, Vec3


class Triangle():
    def __init__(self, v0e, v1e, v2e, Mat):
        self.v0 = v0e
        self.v1 = v1e
        self.v2 = v2e
        self.mat = Mat
        self.normal = self.computeNormal()

    def __str__(self):
        return "({0}, {1}, {2})".format(self.v0, self.v1, self.v2)

    def computeNormal(self):

        v0v1 = self.v1 - self.v0
        v0v2 = self.v2 - self.v0
        return Normalize(Cross(v0v1, v0v2))

    def intersect(self, ray):
        # Returns Tuple: (Hit, distance, normal)
        # Miss object
        miss = (False, 0, Vec3(0, 0, 0))
        normal = Vec3(0, 0, 0)
        v0 = self.v0
        v1 = self.v1
        v2 = self.v2

        v0v1 = v1 - v0
        v0v2 = v2 - v0
        pvec = Cross(ray.d, v0v2)

        det = Dot(v0v1, pvec)

        if det < 0.000001:
            return miss

        invDet = 1.0 / det
        tvec = ray.o - v0
        u = Dot(tvec, pvec) * invDet

        if u < 0 or u > 1:
            return miss

        qvec = Cross(tvec, v0v1)
        v = Dot(ray.d, qvec) * invDet

        if v < 0 or u + v > 1:
            return miss

        return (True, Dot(v0v2, qvec) * invDet, self.normal)


def Copytri(t):
    return Triangle(t.v0, t.v1, t.v2, t.mat)
