import cv2
import numpy as np
import math
from collections import namedtuple

def extract_features(image_path):
    """
    This function extracts the following features from an image at a given path and return those features as
    a namedtuple object.
    Features :-
    1. Aspect Ratio
    2. Leaf Area
    3. Leaf Margin Perimeter
    4. Form Factor
    5. Mean Color
    6. Vein Area Ratio
    7. Elongation
    
    These features can be accessed in the returned namedtuple object by using following attributes on that object :-
    1. aspectratio - Aspect Ratio of Leaf
    2. area - Leaf Area to bounding rectangle area ratio
    3. perimeter - Leaf Perimeter to bounding rectangle perimeter ratio
    4. formfactor - Form Factor
    5. meancolor - Mean Color
    6. veinarea - Ratio of vein area to leaf area
    7. elongation - Measuring the length of the object
    
    arguments:
     image_path - string containing path to leaf image file.
    returns:
     namedtuple object containing extracted features of the leaf.
    """
    # Read image from image file
    bgr_image = cv2.imread(image_path)
    # Obtain RGB and Grayscale images
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    # Apply binary otsu thresholdng to grayscale image
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
    ostu_value, thresh_image = cv2.threshold(gray_image,0, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # Find all contours in thresholded image using RETR_EXTERNAL method
    image_contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find leaf contour among all contours
    leaf_contour = max(image_contours, key=cv2.contourArea) # Contour having maximum area is our leaf contour
    
    # FEATURE - Aspect Ratio
    x, y, w, h = cv2.boundingRect(leaf_contour)
    aspectratio = h / w
    
    # FEATURE - Area
    area = cv2.contourArea(leaf_contour)
    area_ratio = area / (w * h)
    
    # FEATURE - Perimeter
    perimeter = cv2.arcLength(leaf_contour, True)
    perimeter_ratio = perimeter / (2 * (w + h))
    
    # FEATURE - Form Factor
    formfactor = (4 * np.pi * area) / perimeter ** 2
    
    # FEATURE - Mean Color
    # Crop rgb image using bounding rectangle of leaf contour to get leaf portion
    leaf_portion = rgb_image[y:y+h, x:x+w]
    r_mean = int(np.mean(leaf_portion[: ,: ,0])) / 255
    g_mean = int(np.mean(leaf_portion[: ,: ,1])) / 255
    b_mean = int(np.mean(leaf_portion[: ,: ,2])) / 255
    meancolor = (r_mean, g_mean, b_mean)
    
    # FEATURE - Vein Area Ratio
    # Apply sobel filter to image for vein detection
    leaf_portion = cv2.cvtColor(leaf_portion, cv2.COLOR_RGB2GRAY)
    sobel_img = cv2.Sobel(leaf_portion,cv2.CV_64F,1,1,ksize=3)
    sobel_img = np.uint8(sobel_img)
    # Apply Morphological erosion on sobel image
    kernel2 = np.ones((2,1), np.uint8)
    kernel4 = np.ones((4,1), np.uint8)
    erosion2 = cv2.morphologyEx(sobel_img, cv2.MORPH_ERODE, kernel2)
    erosion4 = cv2.morphologyEx(sobel_img, cv2.MORPH_ERODE, kernel4)
    # Calculate ratio of no of non-black pixels to total no of leaf pixels
    non_black_pixels = 0
    for intensity in erosion2.flatten():
        if intensity > 0:
            non_black_pixels += 1
    vein_area_ratio_1 = non_black_pixels / area
    non_black_pixels = 0
    for intensity in erosion4.flatten():
        if intensity > 0:
            non_black_pixels += 1
    vein_area_ratio_2 = non_black_pixels / area

    # FEATURE - Elongation
    minor_axis = min(w,h)
    major_axis = max(w,h)
    elongation = 1 - (minor_axis / major_axis)

    # Create and return namedtuple containing extracted features
    Feature = namedtuple('Feature', ['aspectratio', 'area', 'perimeter', 'formfactor', 'meancolor', 'veinarea1', 'veinarea2', 'elongation'])
    leaf_feature = Feature(
        aspectratio=aspectratio,
        area=area_ratio,
        perimeter=perimeter_ratio,
        formfactor=formfactor,
        meancolor=meancolor,
        veinarea1=vein_area_ratio_1,
        veinarea2=vein_area_ratio_2,
        elongation=elongation)
    return leaf_feature