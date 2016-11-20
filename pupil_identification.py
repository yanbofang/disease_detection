import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_pupil_diameter(img:str):
    image = cv2.imread(img)
    grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    retval, thresholded = cv2.threshold(grayscale, 20, 255, cv2.THRESH_BINARY)
    plt.imsave("binary.png", thresholded)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    # get rid of boundaries
    closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[1:]

    drawing = np.copy(image)
    plt.imsave("eye_contour_original.png", drawing)
    for contour in contours:
        area = cv2.contourArea(contour)
        bounding_box = cv2.boundingRect(contour)
        extend = area / (bounding_box[2] * bounding_box[3])
        
        # get rid of contours with big extend
        if extend > 0.80:
            continue
        
        # calculate centroid and mark
        m = cv2.moments(contour)
        if m['m00'] != 0:
            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            cv2.circle(drawing, center, 3, (0, 255, 0), -1)
        
        # fit an ellipse around contours and draw on pupil
        ellipse = cv2.fitEllipse(contour)
        cv2.ellipse(drawing, box=ellipse, color=(255, 0, 0))

    plt.imsave("eye_contour.png", drawing)
    diameter = 2*(np.sqrt(area/np.pi))/8
    return diameter

def find_eye_diameter(img:str):
    eye = cv2.imread(img)
    return eye.shape[1]

def get_ratio(dia_pupil, length_eye):
    return dia_pupil/length_eye

print(find_pupil_diameter())