import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import re
import plotly.plotly as py
import plotly.graph_objs as go
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
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # get rid of boundaries
    closed = cv2.erode(cv2.dilate(thresh, kernel, iterations=1), kernel, iterations=1)
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[1:]

    drawing = np.copy(image)
    cv2.drawContours(drawing, contours, -1, (255, 0, 0), 1)
    # print(len(contours))

    total_area = 0
    diameter = 0
    largest = (0, 0, 0) # find largest reasonable ellipse (area, Ma, ma)
    for contour in contours:
        area=cv2.contourArea(contour)
        bounding_box = cv2.boundingRect(contour)
        extend = area / (bounding_box[2] * bounding_box[3])

        # get rid of contours with big extend
        if extend > 0.9:
            continue
        
        # calculate centroid and mark
        m = cv2.moments(contour)
        if m['m00'] != 0:
            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            cv2.circle(drawing, center, 3, (0, 255, 0), -1)
        
        # fit an ellipse around contours, find diameter, and draw on pupil
        ellipse = cv2.fitEllipse(contour)
        if ellipse != None:
            (x, y), (MA, ma), angle = ellipse
            ellipse_area = np.pi * MA * ma
            if MA < image.shape[1] * .75 and MA > largest[1]:
                largest = (ellipse_area, MA, ma)
                diameter = MA
                cv2.ellipse(drawing, box=ellipse, color=(255, 100, 255))

    plt.imsave("eye_contour.png", drawing)
    print("Area Ellipse: {} | Major: {} | Minor: {}".format(ellipse_area, MA, ma))
    print("Diameter: {}".format(diameter))
    return diameter

def find_eye_length(img:str):
    eye = cv2.imread(img)
    print("Length: {}".format(eye.shape[1]))
    return eye.shape[1]

def get_ratio(dia_pupil, length_eye):
    return dia_pupil/length_eye

# gives percent if passed in file in format eyeSide_num.png. also generates graph
def percent_of_org(current_file, num:int):
    is_Left = false
    if 'Left' in str(current_file):
        start_file = "eyeLeft_1.png"
        is_Left = true
    else:
        start_file = "eyeRight_1.png"

    start = find_pupil_diameter(start_file)/find_eye_length(start_file)
    current = find_pupil_diameter(current_file)/find_eye_length(current_file)

    per_of_org = (current / start) * 100

    # write information to json
    num = int(re.search(r'\d+', current_file).group())
    with open('data.json') as data_file:    
        data = json.load(data_file)

    if num == 1:
        data = {}

    data[str(num)] = {}

    if is_Left:
        data[str(num)]['left'] = per_of_org
    else:
        data[str(num)]['right'] = per_of_org

    print(str(data))

    with open('data.json', 'w') as outfile:
        json.dump(data, 'data.json')

    generate_graph()

    return per_of_org

def generate_graph():
    with open('data.json') as data_file:    
        data = json.load(data_file)

    x = []
    y1 = []
    y2 = []
    for num in data.keys():
        x.append(num)
        y1.append(data[num]['left'])
        y2.append(data[num]['right'])

    # Create a trace
    trace0 = go.Scatter(
        x = x,
        y = y1,
        mode = 'lines+markers',
        name = 'Left Eye'
    )
    trace1 = go.Scatter(
        x = x,
        y = y2,
        mode = 'lines+markers',
        name = 'Right Eye'
    )
    layout = go.Layout(
        title='Change in Pupil'
    )

    data = [trace0, trace1]
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, filename='graph.png')