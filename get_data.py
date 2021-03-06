import cognitive_face as CF
import scipy
from PIL import Image
import urllib.request

KEY = '88b67a0d6300415e833a263093137907' # subscription key
CF.Key.set(KEY)

def get_images(image:str, num:int):
    faceData = []
    grabImg(image)

    faceData = CF.face.detect(image, face_id = False, landmarks = True)[0]
    faceLandmarks = faceData['faceLandmarks']

    #for right eye
    topLeftX2 = faceLandmarks['eyeRightInner']['x']
    topLeftY2 = faceLandmarks['eyeRightTop']['y']
    bottomRightX2 = faceLandmarks['eyeRightOuter']['x']
    bottomRightY2 = faceLandmarks['eyeRightBottom']['y']
    cropRight(topLeftX2, topLeftY2, bottomRightX2, bottomRightY2, num)
    #for left eye
    topLeftX1 = faceLandmarks['eyeLeftOuter']['x']
    topLeftY1 = faceLandmarks['eyeLeftTop']['y']
    bottomRightX1 = faceLandmarks['eyeLeftInner']['x']
    bottomRightY1 = faceLandmarks['eyeLeftBottom']['y']
    cropLeft(topLeftX1, topLeftY1, bottomRightX1, bottomRightY1, num)

def cropLeft(topLeftX1, topLeftY1, bottomRightX1, bottomRightY1, num:int):
	img = Image.open("face.png")
	imgLeft = img.crop((topLeftX1, topLeftY1, bottomRightX1, bottomRightY1))
	imgLeft.save('eyeLeft_{}.png'.format(num))

def cropRight(topLeftX2, topLeftY2, bottomRightX2, bottomRightY2, num:int):
	img = Image.open("face.png")
	imgRight = img.crop((topLeftX2, topLeftY2, bottomRightX2, bottomRightY2))
	imgRight.save('eyeRight_{}.png'.format(num))

def grabImg(url):
    urllib.request.urlretrieve(url, "face.png")

    # get_images("http://i.imgur.com/Yc7XKtS.png", 1)