#!/usr/bin/env python
 
from http.server import BaseHTTPRequestHandler, HTTPServer
import pupil_identification
import get_data
from urllib.parse import urlparse
import os

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        parsed_path = urlparse(self.path)
        ret = {}
        try:
            self.send_header("Content-type", "image/png")

            params = dict([p.split('=') for p in parsed_path[4].split('&')])
            url = params['face_url']
            image_num = params['num']

            get_images(url) # gets the two eye images, microsoft api

            # right eye
            ret['right_per'] = percent_of_org('eyeRight_{}.png'.format(image_num))
            send_right_img = 'eye_contour.png'
            right_eye = open(send_right_img, 'rb')
            right_stat = os.stat(send_right_img)
            right_size = right_stat.st_size
            f = open(send_right_img, 'rb')
            ret['right_img'] = f.read()
            f.close()

            # left eye
            ret['left_per'] = percent_of_org('eyeLeft_{}.png'.format(image_num))
            send_left_img = 'eye_contour.png'
            left_eye = open(send_left_img, 'rb')
            left_stat = os.stat(send_left_img)
            left_size = left_stat.st_size
            f = open(send_left_img, 'rb')
            ret['left_img'] = f.read()
            f.close()

            # get graph
            graph_img = 'graph.png'
            graph = open(graph_img, 'rb')
            graph_stat = os.stat(graph_img)
            graph_size = left_stat.st_size
            f = open(graph_img, 'rb')
            ret['graph'] = f.read()
            f.close()

            self.wfile.write(str(ret))
        except:
            print("ERROR")
            self.wfile.write(str(ret))
        
        return 

def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8080)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()