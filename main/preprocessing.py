import numpy as np
import cv2
from PIL import Image

def remove_shadow(img_path, output_path):
    # Remove Shadow from Image
    # Read an Image from dataset
    original_img = cv2.imread(img_path)
    # Convert color channels from BGR to RGB
    img2rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    # Apply K-Means to reduce color space in image
    img_pixels = np.float32(img2rgb.reshape((-1, 3)))
    K = 10 # no of clusters
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, K, 1.0)
    ret,labels,centers = cv2.kmeans(img_pixels, K, None, criteria, K, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    cluster_img = centers[labels.flatten()]
    # Set shadow bluish pixels to white
    for i,p in enumerate(cluster_img):
        max_intensity = max(p)
        if max_intensity == p[2]:
            cluster_img[i] = [255, 255, 255]
    cluster_img = cluster_img.reshape(img2rgb.shape)
    cluster_img2gray = cv2.cvtColor(cluster_img, cv2.COLOR_RGB2GRAY)
    retval, th_img = cv2.threshold(cluster_img2gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # Isolate leaf portion in original image
    img = np.bitwise_and(img2rgb, cv2.cvtColor(th_img, cv2.COLOR_GRAY2RGB))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, img)


def resize_image(img_path):
    # Set image dimensions to 700x400
    BOX_WIDTH = 700
    BOX_HEIGHT = 400
    img = Image.open(img_path)
    o_width, o_height = img.size
    ar = o_height / o_width
    r_width = BOX_WIDTH
    r_height = int(BOX_WIDTH * ar)
    resized = img.resize((r_width, r_height), Image.ANTIALIAS)
    if BOX_HEIGHT > r_height:
        # Pad Image
        v_pad = BOX_HEIGHT - r_height
        padding_top = v_pad // 2
        bg = Image.new(resized.mode, (BOX_WIDTH, BOX_HEIGHT), (255,255,255))
        bg.paste(resized, (0, padding_top))
        resized = bg
    elif BOX_HEIGHT < r_height:
        # Crop Image
        left = 0
        right = r_width
        top = (r_height - BOX_HEIGHT) // 2
        bottom = top + BOX_HEIGHT
        resized = resized.crop((left, top, right, bottom))
    resized.save(img_path)