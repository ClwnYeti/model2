from PIL import Image
from math import sqrt

c = 299792458  # Скорость света в м/с


class ImageRefactor:
    def __init__(self, nameOfFile):
        self.nameOfFile = nameOfFile
        self.start_image = Image.open(self.nameOfFile)
        self.waveLengths = {"r": 740e-9, "g": 565e-9, "b": 485e-9}
        self.opticalPowerOfEyes = 14
        self.thicknessOfEyes = 5e-4
        self._B1 = 1.03961212
        self._B2 = 0.231792344
        self._B3 = 1.01046945
        self._C1 = 6.00069867e-15
        self._C2 = 2.00179144e-14
        self._C3 = 103.560653e-12
        self.refractiveIndex = {x: self.refractive_index(self.waveLengths[x]) for x in self.waveLengths.keys()}
        self.focalLength = {x: self.focal_length(self.refractiveIndex[x]) for x in self.refractiveIndex.keys()}
        self.rearDistance = {x: self.rear_distance(self.rear_distance(x)) for x in self.focalLength.keys()}

    def refractive_index(self, waveLength):
        waveLength *= waveLength
        return sqrt(1 + self._B1 * waveLength / (waveLength - self._C1) + self._B2 * waveLength /
                    (waveLength - self._C2) + self._B3 * waveLength / (waveLength - self._C3))

    def focal_length(self, refractive_index):
        return refractive_index / self.opticalPowerOfEyes

    def rear_distance(self, focalLength):
        return focalLength - self.thicknessOfEyes / 2

    def new_coordinate(self, projectionPos, wave):
        return projectionPos * self.focalLength[wave] / self.rearDistance[wave]

    def new_picture(self, newNameForFile=""):
        if newNameForFile == "":
            newNameForFile = "Refactored:" + self.nameOfFile
        newFile = Image.new("RGB", self.start_image.size)




start_image = Image.open("test.png")
objectResolution = min(start_image.get_size()[0], start_image.get_size()[1])


# def getColor(x, y, wavelen):
#     x = x - sensorResolution / 2
#     y = y - sensorResolution / 2
#     x = x / sensorResolution * sensorSize
#     y = y / sensorResolution * sensorSize
#     x = projectionToObject(x, wavelen)
#     y = projectionToObject(y, wavelen)
#     x = round(x / objectSize * objectResolution + objectResolution / 2)
#     y = round(y / objectSize * objectResolution + objectResolution / 2)
#     if (x < 0 or y < 0 or x >= start_image.get_size()[0] or y >= start_image.get_size()[1]):
#         return (0, 0, 0)
#     return start_image.get_at((x, y))[:3]


# def getPixel(x, y):
#     return (getColor(x, y, redWaveLength)[0], getColor(x, y, greenWaveLength)[1], getColor(x, y, blueWaveLength)[2])


