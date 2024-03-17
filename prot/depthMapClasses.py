import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import configparser
import uuid

#Config Loader
config = configparser.ConfigParser()
config.read('config.ini')

class imageBucket : 
    def __init__ (self,pathList): 
        self.images = {}  # Initialize an empty list to store image objects
        for path in pathList:
            id = uuid.uuid4()
            new_image = image(path, id)  # Create an image object
            self.images[id] = new_image # Add the image object to the list

    def display_all_image(self) : 
        for id, image in self.images.items() : 
            image.display_image()

class image: 
    def __init__(self, path, id):
        self.id = id
        self.path = path
        self.load_image(path)

    def load_image(self, path):
        path = 'PXL_20240317_082231220.jpg'
        raw_img = cv.imread(path, cv.IMREAD_GRAYSCALE)
        self.img = raw_img
        # self.process_image(raw_img)
        # try:
        #     raw_img = cv.imread('a.png', cv.IMREAD_GRAYSCALE)
        #     if raw_img is None:
        #         raise FileNotFoundError("Failed to load image.")
        #     self.process_image(raw_img)
        # except Exception as e:
        #     print(f"Error loading image: {e}")

    def process_image(self, raw_img):
        height, width = raw_img.shape[:2]
        size = min(height, width)
        start_x, start_y = (width - size) // 2, (height - size) // 2
        square_img = raw_img[start_y:start_y+size, start_x:start_x+size]
        self.img = cv.resize(square_img, (500, 500), interpolation=cv.INTER_LINEAR)

    def display_image(self) :
        cv.imshow(self.id, self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()




