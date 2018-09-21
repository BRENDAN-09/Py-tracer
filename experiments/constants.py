EPS = 0.001
def getDir(self, x, y, z):
    return (x / self.w * 2 - 1, y / self.h * 2 - 1, -z)
