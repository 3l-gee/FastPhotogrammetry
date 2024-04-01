import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import configparser
import uuid
import os
import random
import util

#DEBUG
import json

#Config Loader
config = configparser.ConfigParser()
config.read('prot/config.ini')
# plt.tick_params(left=False, labelleft=False) #remove ticks
# plt.box(False) #remove box



class ImageBucket : 
    def __init__ (self,directory, pathList): 
        self.images = {}  # Initialize an empty list to store image objects
        self.matches = {}
        for path in pathList:
            fullPath = os.path.join(directory, path)
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
            print(id)
            print(json.dumps(image.keypointsStats, indent=4))

    def filter_all_descriptor(self):
        for id, image in self.images.items() :
            image.filter_descriptor()

    def matcher(self, method = "BF"):
        id1, id2 = util.unique_two_keys(self.images)
        img1, img2 = self.images[id1].img, self.images[id2].img
        key1, key2 = self.images[id1].keypoints, self.images[id2].keypoints
        desc1, desc2 = self.images[id1].descriptors, self.images[id2].descriptors
        if method == "BF" : 

            bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
            matches = bf.match(desc1, desc2)

            good_matches = []
            for m in matches:
                if m.distance < 100000:
                    good_matches.append(m)

            stats = util.match_statistics(good_matches)

            for key, value in stats.items():
                print(f"{key}: {value}")
            
            img3 = cv.drawMatches(
                img1,
                key1,
                img2,
                key2,
                good_matches,
                None,
                flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            plt.imshow(img3),plt.show()
            self.matches[(id1, id2)] = {"matches" : matches, "key1" : key1, "key2" : key2}

        if method == "test2" :
            stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
            disparity_map = stereo.compute(img1, img2)

            # Calculate depth map
            baseline = 1 
            focal_length = 0.5  
            disparity_offset = 0.01
            depth_map = (baseline * focal_length) / (disparity_map + disparity_offset)

             # Display depth map
            plt.imshow(depth_map),plt.show()

        if method == "FLANN" : 
            # Ensure descriptors are in float32 format
            if desc1.dtype != np.float32:
                desc1 = desc1.astype(np.float32)

            if desc2.dtype != np.float32:
                desc2 = desc2.astype(np.float32)

            # FLANN parameters
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks=50)
            
            flann = cv.FlannBasedMatcher(index_params,search_params)
            matches = flann.knnMatch(desc1,desc2,k=2)
            
            pts1_good = []
            pts2_good = []
            pts1 = []
            pts2 = []
            # ratio test as per Lowe's paper
            for i,(m,n) in enumerate(matches):
                pts2.append(key2[m.trainIdx].pt)
                pts1.append(key1[m.queryIdx].pt)
                if m.distance < 0.9*n.distance:
                    pts2_good.append(key2[m.trainIdx].pt)
                    pts1_good.append(key1[m.queryIdx].pt)

            pts1_good = np.int32(pts1_good)
            pts2_good = np.int32(pts2_good)

            util.draw_matches(img1,img2,pts1_good, pts2_good, pts1, pts2)

            F, mask = cv.findFundamentalMat(pts1_good,pts2_good,cv.FM_LMEDS)
 
            # We select only inlier points
            pts1_good = pts1_good[mask.ravel()==1]
            pts2_good = pts2_good[mask.ravel()==1]

            util.draw_matches(img1,img2,pts1_good, pts2_good, pts1, pts2)

            lines1 = cv.computeCorrespondEpilines(pts2_good.reshape(-1,1,2), 2,F)
            lines1 = lines1.reshape(-1,3)
            img5,img6 = util.drawlines(img1,img2,lines1,pts1_good,pts2_good)

            # Find epilines corresponding to points in left image (first image) and
            # drawing its lines on right image
            lines2 = cv.computeCorrespondEpilines(pts1_good.reshape(-1,1,2), 1,F)
            lines2 = lines2.reshape(-1,3)
            img3,img4 = util.drawlines(img2,img1,lines2,pts2_good,pts1_good)
            
            plt.subplot(121),plt.imshow(img5)
            plt.subplot(122),plt.imshow(img3)
            plt.show()

            #Draw good (blue) and bad (red) matching points :
            img3,img4 = util.drawlines(img1,img1,None,pts2_good,pts1_good)
            plt.subplot(121),plt.imshow(img6)
            plt.subplot(122),plt.imshow(img4)
            plt.show()
            self.matches[(id1, id2)] = {"matches" : matches, "key1" : key1, "key2" : key2, "goodPoints" : (pts1_good, pts2_good), "allPoints" : (pts1,pts2)}

    def matching_stats(self, method = "def"):
        if method == "def" : 


            for key, value in  self.matches.items() : 

                points1 = []
                points2 = []
                pts1_pst2_diff = []

                for match in value["matches"]:
                    # Get the keypoints for the matched points
                    keypoint1 = value["key1"][match.queryIdx].pt
                    keypoint2 = value["key2"][match.trainIdx].pt
                    
                    # Append the coordinates to the lists
                    points1.append(keypoint1)
                    points2.append(keypoint2)
                
                    diff = (keypoint1[0] - keypoint2[0], keypoint1[1] - keypoint2[1])
                    pts1_pst2_diff.append(diff)
                # Convert the points to tuples for easier handling
                points1 = [tuple(map(int, point)) for point in points1]
                points2 = [tuple(map(int, point)) for point in points2]

                x1, y1 = zip(*points1)
                x2, y2 = zip(*points2)
                x_mod, y_mod = zip(*pts1_pst2_diff)

                print(x_mod[:10])
                print(y_mod[:10])

                # Plot keypoints for image 1
                # plt.scatter(x1, y1, color='red', label='Image 1 keypoints')

                # # Plot keypoints for image 2 with inverted coordinates
                # plt.scatter(x2, y2, color='blue', label='Image 2 keypoints (inverted)')

                plt.scatter(x_mod, y_mod, color="blue", label = "test")

                plt.xlabel('X')
                plt.ylabel('Y')
                plt.title('KeyPoints Visualization')
                plt.legend()
                plt.show()

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

    def process(self, raw_img):
        height, width = raw_img.shape[:2]
        size = min(height, width)
        start_x, start_y = (width - size) // 2, (height - size) // 2
        square_img = raw_img[start_y:start_y+size, start_x:start_x+size]
        self.img = cv.resize(square_img, (int(height/2), int(width/2)), interpolation=cv.INTER_LANCZOS4)

    def display(self):
        # Convert image from BGR (OpenCV default) to RGB (Matplotlib default)
        imgRGB = cv.cvtColor(self.img, cv.COLOR_BGR2RGB)

        # Check if keypoints are available
        if self.keypoints is not None:
            # Draw keypoints on the image
            imgToShow = cv.drawKeypoints(imgRGB, self.keypoints, None, flags=cv.DRAW_MATCHES_FLAGS_DEFAULT)
        else:
            imgToShow = imgRGB

        # Use Matplotlib to display the image
        plt.figure(figsize=(10, 8))  # You can adjust the figure size as needed
        plt.imshow(imgToShow)
        plt.axis('off')  # Hide axes ticks
        plt.show()

    def compute_descriptor(self, method = "ORB"):
        if method == "ORB":
            orb = cv.ORB_create()
            self.keypoints, self.descriptors = orb.detectAndCompute(self.img, None)
        elif method == "SURF":
            surf = cv.SURF_create()
            self.keypoints, self.descriptors = surf.detectAndCompute(self.img, None)
        elif method == "SIFT":
            sift = cv.SIFT_create()
            self.keypoints, self.descriptors = sift.detectAndCompute(self.img, None)
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
            raise ValueError("Unsupported method. Supported methods: ORB, HARRIS, SURF, SIFT, AKAZE, BRISK, KAZE") 
        
        self.keypointsStats = util.keypoints_statistics(self.keypoints)

            
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




