import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import configparser
import uuid
import exifread
import multiprocessing

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

    def compute_all_descriptors(self,methode) :
        for id, image in self.images.items() :
            image.compute_descriptor(methode)

    def compute_all_descriptor_statistics(self):
        for id, image in self.images.items() :
            image.compute_descriptor_statistics()

    def filter_all_descriptor(self):
        for id, image in self.images.items() :
            image.filter_descriptor()

                    

class Image: 
    def __init__(self, path, id):
        self.id = id
        self.path = path
        self.load_image(path)
        # self.load_metadata(path)
        self.keypoints = None
        self.descriptors = None
        self.keypointsStats = {}

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
        self.img = cv.resize(square_img, (1000,1000), interpolation=cv.INTER_LINEAR)

    def display(self) :
        if self.keypoints is not None :
            imgToShow = cv.drawKeypoints(self.img, self.keypoints, None, flags=cv.DRAW_MATCHES_FLAGS_DEFAULT)
        else : 
            imgToShow  = self.img

        cv.imshow(self.id, imgToShow)
        cv.waitKey(0)
        cv.destroyAllWindows()
        print(self.keypointsStats)

    def compute_descriptor(self, method = "ORB"):
        if method == "ORB":
            orb = cv.ORB_create()
            self.keypoints, self.descriptors = orb.detectAndCompute(self.img, None)
        elif method == "SURF":
            surf = cv.SURF_create()
            self.keypoints = surf.detect(self.img, None)
        elif method == "SIFT":
            sift = cv.SIFT_create()
            self.keypoints = sift.detect(self.img, None)
        elif method == "AKAZE":
            akaze = cv.AKAZE_create()
            self.keypoints, self.descriptors = akaze.detectAndCompute(self.img, None)
        elif method == "BRISK":
            brisk = cv.BRISK_create()
            self.keypoints, self.descriptors = brisk.detectAndCompute(self.img, None)
        elif method == "KAZE":
            kaze = cv.KAZE_create()
            self.keypoints, self.descriptors = kaze.detectAndCompute(self.img, None)
        else:
            raise ValueError("Unsupported method. Supported methods: ORB, SURF, SIFT, AKAZE, BRISK, KAZE") 

            
    def compute_descriptor_statistics(self):     
        num_keypoints = len(self.keypoints)
        if num_keypoints > 0:
            sizes = np.array([keypoint.size for keypoint in self.keypoints])
            mean_size = np.mean(sizes)
            std_size = np.std(sizes)

            orientations = np.array([keypoint.angle for keypoint in self.keypoints])
            mean_orientation = np.mean(orientations)
            std_orientation = np.std(orientations)
        else:
            mean_size = std_size = mean_orientation = std_orientation = np.nan

        # Store statistics in self.keypointsStats
        self.keypointsStats["count"] = num_keypoints
        self.keypointsStats["oriMean"] = mean_orientation
        self.keypointsStats["oriStd"] = std_orientation
        self.keypointsStats["sizeMean"] = mean_size
        self.keypointsStats["sizeStd"] = std_size
        print(self.keypointsStats)

    def filter_descriptor(self, method = "size"):
        if method == "response" :
            self.keypoints = list(self.keypoints)
            self.keypoints.sort(key=lambda kp: kp.response, reverse=True)
            self.keypoints = self.keypoints[:100]
        elif method == "size" :
            self.keypoints = list(self.keypoints)
            self.keypoints.sort(key=lambda kp: kp.size)
            self.keypoints = self.keypoints[:100]




# class Camera :
#     def __init__(self, cameraSepecFile = config['camera']):
#         self.width = 
#         self.height =
#         self.hzResolution =
#         self.vzResolution =
#         self.BitDepth = 
#         self.focalLength =  




