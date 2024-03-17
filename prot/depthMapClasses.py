import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import configparser

#Config Loader
config = configparser.ConfigParser()
config.read('config.ini')

class imageFolder : 
    def __init__ (self,imgScale): 
        self.first 



class image: 
    def __init__(self, path):
        self.path = path
        self.load_image()

    def load_image(self):
        try:
            raw_img = cv.imread(self.path, cv.IMREAD_GRAYSCALE)
            if raw_img is None:
                raise FileNotFoundError("Failed to load image.")
            self.process_image(raw_img)
        except Exception as e:
            print(f"Error loading image: {e}")

    def process_image(self, raw_img):
        height, width = raw_img.shape[:2]
        size = min(height, width)
        start_x, start_y = (width - size) // 2, (height - size) // 2
        square_img = raw_img[start_y:start_y+size, start_x:start_x+size]
        self.img = cv.resize(square_img, (500, 500), interpolation=cv.INTER_LINEAR)

    def display_image(self) :
        cv.imshow('Image', self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()




