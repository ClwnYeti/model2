from PIL import Image
from math import sqrt


class ImageRefactor:
    def __init__(self):
        self.__waveLengths = {"r": 740e-9, "g": 565e-9, "b": 485e-9}
        self.__opticalPowerOfEyes = 20
        self.__screenSize = 0.1
        self.__thicknessOfEyes = 0.1
        self.__B1 = 1.03961212
        self.__B2 = 0.231792344
        self.__B3 = 1.01046945
        self.__C1 = 6.00069867e-15
        self.__C2 = 2.00179144e-14
        self.__C3 = 1.03560653e-10
        self.__refractiveIndex = {x: self.__refractive_index(self.__waveLengths[x]) for x in self.__waveLengths.keys()}
        self.__focalLength = {x: self.__focal_length(self.__refractiveIndex[x]) for x in self.__refractiveIndex.keys()}
        self.__rearDistance = {x: self.__rear_distance(self.__focalLength[x]) for x in self.__focalLength.keys()}

    def new_picture(self, nameOfFile, newNameOfFile=""):
        if newNameOfFile == "":
            newNameOfFile = "refactored-" + nameOfFile
        image = Image.open(nameOfFile)
        width, height = image.size
        newImage = Image.new("RGB", (width, height))
        oldPixels = image.convert("RGB").load()
        red_matrix = self.__new_matrix_for_wave(width, height, oldPixels, "r")
        green_matrix = self.__new_matrix_for_wave(width, height, oldPixels, "g")
        blue_matrix = self.__new_matrix_for_wave(width, height, oldPixels, "b")
        for x in range(width):
            for y in range(height):
                newImage.putpixel((x, y), (red_matrix[x][y], green_matrix[x][y], blue_matrix[x][y]))
        newImage.save(newNameOfFile)

    def __refractive_index(self, waveLength):
        waveLength *= waveLength
        return sqrt(1 + self.__B1 * waveLength / (waveLength - self.__C1) + self.__B2 * waveLength /
                    (waveLength - self.__C2) + self.__B3 * waveLength / (waveLength - self.__C3))

    def __focal_length(self, refractive_index):
        return refractive_index / self.__opticalPowerOfEyes

    def __rear_distance(self, focalLength):
        return focalLength - self.__thicknessOfEyes / 2

    def __new_coordinate(self, projectionPos, wave):
        return projectionPos * self.__focalLength[wave] / self.__rearDistance[wave]

    def __new_matrix_for_wave(self, width, height, pixels, wave):
        matrix = [[0 for i in range(height)] for j in range(width)]
        for x in range(width):
            for y in range(height):
                using_x = self.__new_coordinate(self.__screenSize * (x - width / 2) / width, wave)
                using_x = round(using_x * width / self.__screenSize + width / 2)
                using_y = self.__new_coordinate(self.__screenSize * (y - height / 2) / height, wave)
                using_y = round(using_y * height / self.__screenSize + height / 2)
                if using_y < 0 or using_y >= height or using_x < 0 or using_x >= width:
                    matrix[x][y] = 0
                else:
                    if wave == "r":
                        matrix[x][y] = pixels[using_x, using_y][0]
                    elif wave == "g":
                        matrix[x][y] = pixels[using_x, using_y][1]
                    else:
                        matrix[x][y] = pixels[using_x, using_y][2]
        return matrix


refactor = ImageRefactor()
refactor.new_picture("test2.jpg")









