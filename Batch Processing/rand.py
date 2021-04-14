import os
import sys
import cv2
import numpy as np
import random

file_path = sys.argv[1]
image = cv2.imread("./in/" + file_path)



def findClosest(pixel_value, palette):
    """
    Given a palette (an array of rgb values stored as tuples or lists) and a
    pixel value (tuple or list of rgb values), return the closest color in the palette
    and the distance of each rgb value in pixel_value from that color.
    """
    error_array, total_array = [], []
    i = 0
    for color in palette:
        error_array.append([])
        for channel_index in range(len(pixel_value)):
            error_array[i].append(pixel_value[channel_index]-color[channel_index])
        total_error = 0
        for error in error_array[i]:
            total_error += abs(float(error))
        total_array.append(total_error)
        i += 1
    min_index = total_array.index(min(total_array))
    return palette[min_index], error_array[min_index]

class Steinberg:
    def __init__(self, image):
        self.image = image
        self.width, self.height = self.image.shape[0], self.image.shape[1]
        self.divisor = 16.0

        # The error diffusion values
        self.MR = 7.0
        self.BL = 3.0; self.BM = 5.0; self.BR = 1.0
      
    def generatePalette(self):
        self.palette = []
        num_colors = (int(sys.argv[2]))
        for i in range(num_colors):
            pixel = self.image[random.randint(0, self.width-1), random.randint(0, self.height-1)]
            self.palette.append((pixel[0], pixel[1], pixel[2]))

    def dither(self):
        """
        Apply a Steinberg dither on the class's image. The image is overwritten.
        """
        self.generatePalette()
        print('\nLoading...')
        error_array = np.zeros((self.width, self.height, 3))
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.image[x, y]
                pixel_value = [pixel[0], pixel[1], pixel[2]]
                for i in range(len(pixel_value)):
                    pixel_value[i] += error_array[x][y][i]
                pixel_value, error = findClosest(pixel_value, self.palette)
                self.image[x, y] = pixel_value
                try:
                    for channel_index in range(len(error_array[x+1, y])):
                        error_array[x+1, y][channel_index] = self.MR / self.divisor * error[channel_index]
                except:
                    pass
                try:
                    for channel_index in range(len(error_array[x-1, y+1])):
                        error_array[x-1, y+1][channel_index] = self.BL / self.divisor * error[channel_index]
                except:
                    pass
                try:
                    for channel_index in range(len(error_array[x, y+1])):
                        error_array[x, y+1][channel_index] = self.BM / self.divisor * error[channel_index]
                except:
                    pass
                try:
                    for channel_index in range(len(error_array[x+1, y+1])):
                        error_array[x+1, y+1][channel_index] = self.BR / self.divisor * error[channel_index]
                except:
                    pass
                
    def show(self):
        split = os.path.splitext(file_path)
        cv2.imwrite("./out/dither_PRand"+ sys.argv[2] + "-" + split[0] + '.png', self.image)
        print('Saved dither_PRand'+ sys.argv[2] + "-" + split[0] + '.png to out folder.')
        sys.exit()
        
ditherer = Steinberg(image) 
ditherer.dither()

print('Done')
ditherer.show()

