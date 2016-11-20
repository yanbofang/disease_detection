#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
from pupil_identification import percent_of_org
from get_data import get_images
from urllib.parse import urlparse
import os, json, base64
from dataIO import fileIO

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        parsed_path = urlparse(self.path)
        ret = {}

        self.send_header("Content-type", "image/png")

        params = dict([p.split('=') for p in parsed_path[4].split('&')])
        url = params['face_url']
        image_num = params['num']

        get_images(url, image_num) # gets the two eye images, microsoft api

        # right eye
        ret['right_per'] = percent_of_org('eyeRight_{}.png'.format(image_num), image_num)
        send_right_img = 'eye_contour.png'
        right_eye = open(send_right_img, encoding='latin-1')
        right_stat = os.stat(send_right_img)
        right_size = right_stat.st_size
        f = open(send_right_img, encoding='latin-1')
        ret['right_img'] = f.read()
        f.close()

        # left eye
        ret['left_per'] = percent_of_org('eyeLeft_{}.png'.format(image_num), image_num)
        send_left_img = 'eye_contour.png'
        left_eye = open(send_left_img, encoding='latin-1')
        left_stat = os.stat(send_left_img)
        left_size = left_stat.st_size
        f = open(send_left_img, encoding='latin-1')
        ret['left_img'] = f.read()
        f.close()

        # get graph
        graph_img = 'graph.png'
        graph = open(graph_img, encoding='latin-1')
        graph_stat = os.stat(graph_img)
        graph_size = left_stat.st_size
        f = open(graph_img, encoding='latin-1')
        ret['graph'] = f.read()
        f.close()

        # graph data
        ret["graph_data"] = fileIO("data.json", "load")

        #ret_file = "return.json"
        #if not fileIO(ret_file, "check"):
        #    fileIO(ret_file, "save", ret)
        #ret = fileIO(ret_file, "load")
        
        self.wfile.write(bytes(str(ret), 'latin-1'))
        
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