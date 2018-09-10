from Vector3 import Vec3, Cross, Normalize
from random import random
from math import pi, sin, cos

normal = Normalize(Vec3(1, 0, 0))
f = open("data.dat", "w")


def diskPoint():
    theta = random() * pi * 2
    mag = random()
    x = cos(theta) * mag
    y = sin(theta) * mag
    return Vec3(x, y, 0)


for i in range(1000):
    p = diskPoint()
    f.write("{0}  {1}\n".format(p.x, p.y))
    w = normal
    v = Cross(Vec3(0.00319, 0.0078, 1.0), w)  # jittered up
    v = Normalize(v)  # normalize
    u = Cross(v, w)

    hemi_dir = (u ^ p.x) + (v ^ p.y) + (w ^ p.z)
    hemi_dir = Normalize(hemi_dir)
    # f.write("{0}   {1}   {2}\n".format(hemi_dir.x, hemi_dir.y, hemi_dir.z))
    print(Normalize(hemi_dir))
