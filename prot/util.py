import random
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def unique_two_keys(dic):
    """
    Picks two different keys from a dictionary.
    
    Args:
        dic (dict): The dictionary from which to pick keys.
        
    Returns:
        tuple: A tuple containing two different keys from the dictionary.
    """
    keys = list(dic.keys())
    chosen_keys = random.sample(keys, 2)
    return chosen_keys[0], chosen_keys[1]


def drawlines(img1,img2,lines,pts1,pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
    lines - corresponding epilines '''
    r,c = img1.shape
    img1 = cv.cvtColor(img1,cv.COLOR_GRAY2BGR)
    img2 = cv.cvtColor(img2,cv.COLOR_GRAY2BGR)
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv.line(img1, (x0,y0), (x1,y1), color,1)
        img1 = cv.circle(img1,tuple(pt1),5,color,-1)
        img2 = cv.circle(img2,tuple(pt2),5,color,-1)
    return img1,img2


def match_statistics(matches):
    """
    Calculates statistical data from matches.

    Args:
        matches (list): List of DMatch objects representing matches.

    Returns:
        dict: Dictionary containing statistical data.
    """
    num_matches = len(matches)  # Total number of matches

    if num_matches == 0:
        return {
            'num_matches': 0,
            'average_distance': None,
            'max_distance': None,
            'min_distance': None,
            'mean_distance': None,
            'std_deviation': None
        }

    # Calculate distances between matches
    distances = [match.distance for match in matches]

    # Calculate statistical measures
    sum_distances = sum(distances)
    average_distance = sum_distances / num_matches
    max_distance = max(distances)
    min_distance = min(distances)
    
    # Calculate mean distance
    mean_distance = sum_distances / num_matches

    # Calculate standard deviation
    sum_squared_diff = sum((distance - mean_distance) ** 2 for distance in distances)
    variance = sum_squared_diff / num_matches
    std_deviation = variance ** 0.5

    # Construct dictionary with statistical data
    statistics = {
        'num_matches': num_matches,
        'average_distance': average_distance,
        'max_distance': max_distance,
        'min_distance': min_distance,
        'mean_distance': mean_distance,
        'std_deviation': std_deviation
    }

    return statistics

def keypoints_statistics(keypoints):    
    res = {} 
    num_keypoints = len(keypoints)
    if num_keypoints > 0:
        sizes = np.array([keypoint.size for keypoint in keypoints])
        mean_size = np.mean(sizes)
        std_size = np.std(sizes)

        orientations = np.array([keypoint.angle for keypoint in keypoints])
        mean_orientation = np.mean(orientations)
        std_orientation = np.std(orientations)
    else:
        mean_size = std_size = mean_orientation = std_orientation = np.nan

    # Store statistics in res
    res = {
        "count": num_keypoints,
        "oriMean": mean_orientation,
        "oriStd": std_orientation,
        "sizeMean": mean_size,
        "sizeStd": std_size
    }

    return res

def draw_matches(img1, img2, pts1_good, pts2_good, pts1, pts2):
    # Create copies of the images to draw on so we don't alter the originals
    img1_draw = cv.cvtColor(img1.copy(), cv.COLOR_GRAY2RGB)
    img2_draw = cv.cvtColor(img2.copy(), cv.COLOR_GRAY2RGB)

    # Draw all points in red
    for pt in pts1:
        cv.circle(img1_draw, (int(pt[0]), int(pt[1])), 2, (0, 0, 255), -1)
    for pt in pts2:
        cv.circle(img2_draw, (int(pt[0]), int(pt[1])), 2, (0, 0, 255), -1)

    # # Draw good points in blue
    for pt in pts1_good:
        cv.circle(img1_draw, (int(pt[0]), int(pt[1])), 2, (255, 0, 0), -1)
    for pt in pts2_good:
        cv.circle(img2_draw, (int(pt[0]), int(pt[1])), 2, (255, 0, 0), -1)

    # # Combine images for side-by-side comparison
    combined_img = np.hstack((img1_draw, img2_draw))

    # Use matplotlib to display the image

    plt.figure(figsize=(15, 10))
    plt.imshow(cv.cvtColor(combined_img, cv.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()