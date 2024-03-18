import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import configparser
import uuid
# import exifread

#Config Loader
config = configparser.ConfigParser()
config.read('prot/config.ini')

class ImageBucket : 
    def __init__ (self,pathList, directory): 
        self.images = {}  # Initialize an empty list to store image objects
        for path in pathList:
            fullPath = str(directory + "/" + path)
            id = str(uuid.uuid4())
            new_image = Image(fullPath, id)  # Create an image object
            self.images[id] = new_image # Add the image object to the list

    def display_all_image(self) : 
        for id, image in self.images.items() : 
            image.display()

    def compute_all_descriptors(self) :
        for id, image in self.images.items() :
            image.compute_descriptor()

class Image: 
    def __init__(self, path, id):
        self.id = id
        self.path = path
        self.load_image(path)
        # self.load_metadata(path)
        self.keypoints = None
        self.descriptors = None

    def load_image(self, path):
        try:
            raw_img = cv.imread(path, cv.IMREAD_GRAYSCALE)
            if raw_img is None:
                raise FileNotFoundError("Failed to load image.")
            self.process(raw_img)
        except Exception as e:
            print(f"Error loading image: {e}")

    # def load_metadata(self, path):
    #     with open(path, 'rb') as f:
    #         tags = exifread.process_file(f)
    #         self.img_metadata = {
    #             'Camera Model': tags.get('Image Model'),
    #             'Image Size': tags.get('Image ImageSize'),
    #             'Exposure Time': tags.get('EXIF ExposureTime'),
    #             'Aperture': tags.get('EXIF FNumber'),
    #             'ISO': tags.get('EXIF ISOSpeedRatings'),
    #             'Focal Length': tags.get('EXIF FocalLength'),
    #         }
    #         f.close()

    def process(self, raw_img):
        height, width = raw_img.shape[:2]
        size = min(height, width)
        start_x, start_y = (width - size) // 2, (height - size) // 2
        square_img = raw_img[start_y:start_y+size, start_x:start_x+size]
        self.img = cv.resize(square_img, (2000,2000), interpolation=cv.INTER_LINEAR)

    def display(self) :
        if self.keypoints is not None and self.descriptors is not None:
            imgToShow = cv.drawKeypoints(self.img, self.keypoints, None, flags=cv.DRAW_MATCHES_FLAGS_DEFAULT)
        else : 
            imgToShow  = self.img

        cv.imshow(self.id, imgToShow)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def compute_descriptor(self):
        orb = cv.ORB_create()
        self.keypoints, self.descriptors = orb.detectAndCompute(self.img, None)


# class Camera :
#     def __init__(self, cameraSepecFile = config['camera']):
#         self.width = 
#         self.height =
#         self.hzResolution =
#         self.vzResolution =
#         self.BitDepth = 
#         self.focalLength =  




