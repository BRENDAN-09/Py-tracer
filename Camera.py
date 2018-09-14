# Camera.py
import array
from Vector3 import Vec3, Normalize, Cross
from Ray import Ray
from Diffuse import OrientedHemiDir
from random import random
from math import sin, cos


class Camera:
    def __init__(self, Pos, W, H, Fov=1, Samples=256):
        self.fov = Fov
        self.w = W
        self.h = H
        self.pos = Pos
        self.samples = Samples
        self.normal = Vec3(0, 0, -1)
        self.bgColor = Vec3(0.58, 0.74, 1)
        self.target = Vec3(0, 0, 0)
        self.image_array = array.array(
            'B', [0] * (W * H * 3))
        self.ca = self.setCamera(self.pos, self.target, 0)

    def lookAt(self, pos):
        self.target = pos
        self.ca = self.setCamera(self.pos, self.target, 0)

    def savePixel(self, single_pixel, x, y):
        # convert 0-1 to 0-255
        pixel = single_pixel ^ 255
        # clamp pixel
        pixel.clamp(0.0, 255.0)
        # write to array
        i = ((self.h - y - 1) * self.w + x)
        self.image_array[i * 3 + 0] = int(pixel.x)
        self.image_array[i * 3 + 1] = int(pixel.y)
        self.image_array[i * 3 + 2] = int(pixel.z)

    def getDir(self, x, y, z):
        # calculate direction
        d = Vec3(x / self.w * 2 - 1, y / self.h * 2 - 1, 1)
        d = Normalize(d)
        # Rotate to match camera rotation
        return self.multMat(self.ca, d)

    def setCamera(self, ro, ta, cr):
        cw = Normalize(ta - ro)
        cp = Vec3(sin(cr), cos(cr), 0.0)
        cu = Normalize(Cross(cw, cp))
        cv = Normalize(Cross(cu, cw))
        return [cu, cv, cw]

    def multMat(self, mat, vec):
        out = Vec3(0, 0, 0)
        dimensions = ["x", "y", "z"]
        for i in range(3):
            out = out + (mat[i] ^ getattr(vec, dimensions[i]))
        return out

    # save pixel array to file
    def saveImage(self, filename):
        # create image file
        image = open(filename, 'wb')
        # write magic number, and filename
        image.write(("P6\n#" + filename).encode())
        # write image width, height and max colour-component value
        image.write(("\n" + str(self.w) + " " +
                     str(self.h) + "\n255\n").encode())
        # write image_array to .ppm file
        image.write(self.image_array.tostring())
        # close .ppm file
        image.close()
        print("Image Saved")

    def render(self, tracer):
        # loop through all the pixels in the image
        for x in range(self.w):
            for y in range(self.h):
                col = Vec3(0, 0, 0)
                # average the samples
                for i in range(self.samples):
                    # calculate direction
                    # Adds the random to get anti-aliasing
                    a = self.getDir(x + random(), y + random(), 1)
                    # create ray for rendering
                    ray = Ray(orig=self.pos, dir=a)
                    # render!
                    col = col + self.rendererCalcColor(ray, 4, tracer)
                col = col ^ (1 / self.samples)  # average the samples
                self.savePixel(col, x, y)  # save pixel
            print("{0} percent done".format(x / self.w * 100))
        self.saveImage("gi.ppm")  # save image

    def rendererCalcColor(self, ray, numBounce, tracer):
        tCol = Vec3(0, 0, 0)
        fCol = Vec3(1, 1, 1)

        for i in range(numBounce):
            # intersect with seen
            isec = tracer.worldIntersect(ray)
            # intersection information
            sec = isec["t"]
            # if no intersection
            if not sec[0]:
                # stop the accumulation process or return the sky
                if i == 0:
                    return self.bgColor
                else:
                    break
            # Calculate intersection position
            pos = ray.o + (ray.d ^ sec[1])
            # load material
            material = isec["index"].mat
            # Load surface colour and compute direct lighting
            sCol = tracer.materials[material]
            dCol = self.applyDirectLighting(pos, sec[2], tracer)
            # Create new ray
            ray = Ray(orig=pos + (sec[2] ^ 0.1),
                      dir=OrientedHemiDir(sec[2]))
            # accumulate colours
            fCol = sCol * fCol
            tCol += fCol * dCol
        return tCol

    def applyDirectLighting(self, pos, nor, scene):
        dCol = Vec3(0, 0, 0)
        for i in scene.lights:
            dCol += i.calcDirect(pos, nor, scene)
        return dCol
