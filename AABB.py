# AABB.py
# Axis Aligned Bounding Box
from Vector3 import Vec3
from Ray import Ray


class AABB():
    def __init__(self, Min, Max):
        self.min = Min
        self.max = Max

    def intersect(self, ray):
        b = ray.d.x
        if b == 0:
            b += 0.000001
        tmin = (self.min.x - ray.o.x) / b
        tmax = (self.max.x - ray.o.x) / b
        if tmin > tmax:
            tmin, tmax = tmax, tmin
        for a in ["y", "z"]:
            b = getattr(ray.d, a)
            if b == 0:
                b += 0.000001
            tymin = (getattr(self.min, a) - getattr(ray.o, a)) / \
                b
            tymax = (getattr(self.max, a) - getattr(ray.o, a)) / \
                b
            # Swap if necessary
            if tymin > tymax:
                tymin, tymax = tymax, tymin
            # Check collision
            if (tmin > tymax) or (tymin > tmax):
                return False
            # Update tmin and tmax
            tmin = min(tmin, tymin)
            tmax = max(tmax, tymax)
        return True

aabb = AABB(Vec3(-1, -1, -1), Vec3(1, 1, 1))
ray = Ray(orig=Vec3(0, 0, -3), dir=Vec3(0, 0, -2))
z = aabb.intersect(ray)
print(z)
