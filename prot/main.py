import depthMapClasses as DMC
import cv2 as cv
import os
# imageList1 = [
#     'PXL_20240317_082231220.jpg',
#     'PXL_20240317_082234839.jpg',
#     ]

# imageBucket1 = DMC.imageBucket(imageList1)

# imageBucket1.display_all_image()

file = 'img\PXL_20240317_082231220.jpg'
assert os.path.exists(file)

test = cv.imread(file)