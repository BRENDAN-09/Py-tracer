# Camera.py
import array
from Vector3 import Vec3, Normalize, Cross
from Ray import Ray
from Diffuse import OrientedHemiDir
from random import random
from math import sin, cos
import os


class Camera:
    def __init__(self, Pos, W, H, Fov=1, Samples=256):
        """
        Initialises a Camera class.
        Parameters:
            Pos: Vec3. The position of the camera
            W: Float. The camera width
            H: Float. The camera height
        Optional Parameters:
            Fov: Float. The field of view constant of the camera. Default 1.
            Samples: Int. The rendering sample rate. Deafault 256
        """
        # Init variables
        self.fov = Fov
        self.w = W  # Width
        self.h = H  # Height
        self.pos = Pos  # Camera position
        self.samples = Samples  # Sample Rate
        self.normal = Vec3(0, 0, -1)  # Normal (used for rotation)
        self.bgColor = Vec3(0.58, 0.74, 1)  # background colour
        self.target = Vec3(0, 0, 0)  # Camera target, used for rotation
        self.barWidth = 50  # progress bar width
        self.image_array = array.array(
            'B', [0] * (W * H * 3))  # Array for image data
        # set rotation matrix
        self.ca = self.setCamera()

    def lookAt(self, pos):
        """
        Updates the rotation matrix so that the camera is looking
        at a certain point
        Parameters:
            Pos: Vec3. The point to look at
        """
        # set the position
        self.target = pos
        self.ca = self.setCamera()

    def savePixel(self, single_pixel, x, y):
        """
        Saves a pixel to the camera's image_array.
        Parameters:
            single_pixel: The pixel to be saved
            x: The x coordinates to save it at
            y: The y coordinates to save it at
        """
        # convert 0-1 to 0-255
        pixel = single_pixel ^ 255
        # clamp pixel
        pixel.clamp(0.0, 255.0)
        # write to array
        i = ((self.h - y - 1) * self.w + x)
        self.image_array[i * 3 + 0] = int(pixel.x)
        self.image_array[i * 3 + 1] = int(pixel.y)
        self.image_array[i * 3 + 2] = int(pixel.z)

    def getDir(self, x, y):
        """
        Get direction from pixel coordinates
        Parameters:
            x: The pixel's x coordinates
            y: The pixel's y coordinates
        """
        # calculate direction
        d = Vec3(x / self.w * 2 - 1, y / self.h * 2 - 1, 1)
        d = Normalize(d)
        # Rotate to match camera rotation
        return self.multMat(self.ca, d)

    def setCamera(self):
        """
        Updates the camera's rotation matrix
        """
        ro = self.pos  # ray origin
        ta = self.target  # ray target
        cr = 0  # Angular rotation (should always be 0)
        # Construct the matix using some fancy linear algebra
        cw = Normalize(ta - ro)
        cp = Vec3(sin(cr), cos(cr), 0.0)
        cu = Normalize(Cross(cw, cp))
        cv = Normalize(Cross(cu, cw))
        return [cu, cv, cw]

    def multMat(self, mat, vec):
        """
        Multiplies a Vec3 by a matrix.
        Parameters:
            mat: List<Vec3>. The matrix to be multiplied
            vec: Vec3. The vector to be multiplied
        """
        # Initialise the output vector
        out = Vec3(0, 0, 0)
        # iterate through the dimensions
        dimensions = ["x", "y", "z"]
        for i in range(3):
            out = out + (mat[i] ^ getattr(vec, dimensions[i]))
        return out

    def saveImage(self, filename):
        """
        Saves an image to a ppm file.
        Parameters:
            filename: String. The name of the file to be saved
        """
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

    def render(self, tracer, imgOut):
        """
        Renders a scene to an image
        Parameters:
            tracer: Scene. The scene to be rendered.
            imgOut: String. The name of the output file
        """
        # loop through all the pixels in the image
        for x in range(self.w):
            for y in range(self.h):
                col = Vec3(0, 0, 0)
                # Aspect correction in the case the output image is not square
                mx = x * self.w/self.h
                # average the samples
                for i in range(self.samples):
                    # calculate direction
                    # Adds the random to get anti-aliasing
                    a = self.getDir(mx + random(), y + random())
                    # create ray for rendering
                    ray = Ray(orig=self.pos, dir=a)
                    # render!
                    col = col + self.rendererCalcColor(ray, 4, tracer)
                col = col ^ (1 / self.samples)  # average the samples
                self.savePixel(col, x, y)  # save pixel
            # ===Update progress bar===
            # Clear terminal
            os.system('cls' if os.name == 'nt' else 'clear')
            # Calculate progress
            prog = int(round((x) / self.w * self.barWidth))
            # Print progress bar
            print("[" + "=" * prog + ">" + " " * (self.barWidth - prog) + "] " +
                  str(round(prog * (100 / self.barWidth))) +
                  "% completed")
        # ===Save Image===
        self.saveImage(imgOut)  # save image

    def rendererCalcColor(self, ray, numBounce, tracer):
        """
        Calculates a pixel colour given a starting ray using Monte Carlo magik!
        Parameters:
            ray: Ray. The ray to be traced
            numBounce: Int. The number of bounces the ray is allowed to do
            tracer: Scene. The scene
        """
        # Variables for colour accumulation
        tCol = Vec3(0, 0, 0)
        gCol = Vec3(1, 1, 1)

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
            gCol = sCol * gCol
            tCol += gCol * dCol
        # return the total colour
        return tCol

    def applyDirectLighting(self, pos, nor, scene):
        """
        Applies Direct lighting
        Parameters:
            pos: Vec3. The point to apply the direct lighting
            nor: Vec3. The surface normal.
            scene: Scene. The scene.
        """
        # start the accumulation
        dCol = Vec3(0, 0, 0)
        # iterate over lights and accumulate colors
        for i in scene.lights:
            dCol += i.calcDirect(pos, nor, scene)
        return dCol
