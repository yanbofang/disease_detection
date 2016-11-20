import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance

def find_pupil_diameter(img:str):
    # increase image contrast
    image = Image.open(img)
    contrast = ImageEnhance.Contrast(image)
    new_image = contrast.enhance(1.2)
    new_image.save("contrast_image.png")

    # opencv processing
    image = cv2.imread("contrast_image.png")
    grayscale = np.copy(image)
    grayscale = cv2.cvtColor(grayscale, cv2.COLOR_RGB2GRAY)
    plt.imsave("image_test.png", image)    
    ret, thresh = cv2.threshold(grayscale, 30, 255, cv2.THRESH_BINARY)
    plt.imsave("binary.png", thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # get rid of boundaries
    closed = cv2.erode(cv2.dilate(thresh, kernel, iterations=1), kernel, iterations=1)
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[1:]

    drawing = np.copy(image)
    plt.imsave("eye_contour_original.png", drawing)
    cv2.drawContours(drawing, contours, -1, (255, 0, 0), 1)
    print(len(contours))
    total_area = 0
    for contour in contours:
        area=cv2.contourArea(contour)
        bounding_box = cv2.boundingRect(contour)
        extend = area / (bounding_box[2] * bounding_box[3])
        
        print("Area: {}".format(area))
        # get rid of contours with big extend
        if extend > 0.9:
            continue
        
        # calculate centroid and mark
        m = cv2.moments(contour)
        if m['m00'] != 0:
            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            cv2.circle(drawing, center, 3, (0, 255, 0), -1)
        
        # fit an ellipse around contours, find diameter, and draw on pupil
        diameter = 0
        ellipse = cv2.fitEllipse(contour)
        if ellipse != None:
            (x, y), (MA, ma), angle = ellipse
            ellipse_area = np.pi * MA * ma
            print("Area Ellipse: {} | Major: {} | Minor: {}".format(ellipse_area, MA, ma))
            diameter = MA
            cv2.ellipse(drawing, box=ellipse, color=(255, 100, 255))

    plt.imsave("eye_contour.png", drawing)
    print("Diameter: {}".format(diameter))
    return diameter

def find_eye_length(img:str):
    eye = cv2.imread(img)
    return eye.shape[1]

def get_ratio(dia_pupil, length_eye):
    return dia_pupil/length_eye

rightEye_file = "right_2.png"
leftEye_file = "left_2.png"
rightEye_dia = "imgRight_dia.png"
other_file = "eye.png"

diameter = find_pupil_diameter(rightEye_file)
eye_length = find_eye_length(rightEye_file)
ratio = get_ratio(diameter, eye_length)
print(ratio)