import cognitive_face as CF
import scipy

KEY = '88b67a0d6300415e833a263093137907' # subscription key
CF.Key.set(KEY)

def get_data():
    
    image = "http://i.imgur.com/4boKR9E.png"
    print(CF.face.detect(image)[0])

get_data()