import depthMapClasses as DMC

directory = 'img'
imageList1 = [
    "PXL_20240317_082245096.jpg",
    "PXL_20240317_082249759.jpg"
    ]

imageBucket1 = DMC.ImageBucket(directory,imageList1)

imageBucket1.compute_all_descriptors("AKAZE")

imageBucket1.compute_all_descriptor_statistics()

imageBucket1.display_all_image()

imageBucket1.matcher("FLANN")

imageBucket1.matching_stats()
