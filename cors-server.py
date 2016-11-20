from http.server import BaseHTTPRequestHandler, HTTPServer
from pupil_identification import percent_of_org
from get_data import get_images
from urllib.parse import urlparse
import os, json, base64, http.server, re
from flask import Flask
from flask_cors import CORS, cross_origin
from dataIO import fileIO

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        """Common code for GET and HEAD commands.
        This sends the response code and MIME headers.
        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.
        """

        # Send response status code
        self.send_response(200)

        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "image/png")

        image_num = re.sub("[^0-9]", "", str(self.path).rsplit('/', 1)[-1])

        url = 'http://minh.heliohost.org/detection_disease/uploads/face{}.png'.format(image_num)
        ret = {}

        get_images(url, image_num) # gets the two eye images, microsoft api

        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "image/png")

        # right eye
        ret['right_per'] = percent_of_org('eyeRight_{}.png'.format(image_num), image_num)
        send_right_img = 'eye_contour.png'
        right_eye = open(send_right_img, encoding='latin-1')
        right_stat = os.stat(send_right_img)
        right_size = right_stat.st_size
        f = open(send_right_img, encoding='latin-1')
        # ret['right_img'] = f.read()
        f.close()

        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "image/png")

        # left eye
        ret['left_per'] = percent_of_org('eyeLeft_{}.png'.format(image_num), image_num)
        send_left_img = 'eye_contour.png'
        left_eye = open(send_left_img, encoding='latin-1')
        left_stat = os.stat(send_left_img)
        left_size = left_stat.st_size
        f = open(send_left_img, encoding='latin-1')
        # ret['left_img'] = f.read()
        f.close()

        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "image/png")
        
        # get graph
        graph_img = 'graph.png'
        graph = open(graph_img, encoding='latin-1')
        graph_stat = os.stat(graph_img)
        graph_size = left_stat.st_size
        f = open(graph_img, encoding='latin-1')
        # ret['graph'] = f.read()
        f.close()

        # graph data
        ret["graph_data"] = fileIO("data.json", "load")

        #ret_file = "return.json"
        #if not fileIO(ret_file, "check"):
        #    fileIO(ret_file, "save", ret)
        #ret = fileIO(ret_file, "load")
        
        self.wfile.write(bytes(str(ret), 'latin-1'))
        
        return

if __name__ == "__main__":
    import os
    import socketserver

    PORT = 31338

    Handler = CORSHTTPRequestHandler
    #Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = socketserver.TCPServer(("", PORT), Handler)

    print("serving at port", PORT)
    httpd.serve_forever()