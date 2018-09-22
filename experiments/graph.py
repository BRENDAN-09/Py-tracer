from Diffuse import orthonormal, diskPoint
from Vector3 import Vec3

file = open("data.dat", "w")

for i in range(1000):
    a = diskPoint()
    file.write("{0}   {1}\n".format(a.x, a[1]))
