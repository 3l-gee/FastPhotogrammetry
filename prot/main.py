import depthMapClasses as DMC
import cv2 as cv
import os

directory = 'prot/img'
imageList1 = [
    'PXL_20240317_082231220.jpg',
    'PXL_20240317_082234839.jpg',
    'PXL_20240317_082239261.jpg',
    'PXL_20240317_082245096.jpg',
    'PXL_20240317_082249759.jpg',
    'PXL_20240317_082254819.jpg',
    'PXL_20240317_082303565.jpg',
    'PXL_20240317_082309262.jpg',
    'PXL_20240317_082319750.jpg',
    'PXL_20240317_082324792.jpg',
    ]

imageBucket1 = DMC.ImageBucket(imageList1,directory)

imageBucket1.compute_all_descriptors("KAZE")

imageBucket1.compute_all_descriptor_statistics()

imageBucket1.filter_all_descriptor()

imageBucket1.compute_all_descriptor_statistics()

imageBucket1.display_all_image()

