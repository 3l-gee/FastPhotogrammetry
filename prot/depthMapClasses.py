import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import configparser

#Config Loader
config = configparser.ConfigParser()
config.read('config.ini')
print(config.sections())

class imageProcesssor: 
    def __init__ (self,imgScale ): 
        self.imgScale



class image: 
    def __init__ (self, path):
        self.img = cv.imread(path, cv.IMREAD_GRAYSCALE)
        self.path = path



