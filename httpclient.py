#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
import pdb  
# you may use urllib to encode data appropriately
from urllib.parse import urlparse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.socket.connect((host, port))
        return self.socket

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def read_result(self, data):
        print("Log: DATA\n", data)
        try:
            temp = data.splitlines()[0]
            temp2 = temp.split(' ', 2)
            resp_code = int(temp2[1])
            resp_mess = temp2[2]
            i = data.splitlines().index('')
            t = data.splitlines()[i:]
            resp_body = ''
            for b in t:
                resp_body += b
            return resp_code, resp_mess, resp_body
        except Exception as e:
            return ("Log: Some other error in read_result. ", e)

    def GET(self, url, args=None):
        new_rl = urlparse(url)
        host = new_rl.hostname
        port = new_rl.port
        path = new_rl.path
        if not port:
            port = 80

        sock = self.connect(host, port)
        header = "GET "+path+" HTTP/1.1\r\nHost: "+host+"\r\n\r\n"
        if not sock.sendall(header.encode()):
            data = self.recvall(sock)
            c, m, b = self.read_result(data)
            return HTTPResponse(code=c, body=b)
        else:
            return ("Error in GET method")

    def POST(self, url, args=None):
        new_rl = urlparse(url)
        host = new_rl.hostname
        port = new_rl.port
        path = new_rl.path
        if not port:
            port = 80

        header = "POST "+path+" HTTP/1.1\r\nHost: "+host+"\r\n"
        header += "User-Agent: Mozilla/5.0\r\n"
        header += "Accept: */*\r\n"
        header += "Accept-Language: en-US, en; q=0.5\r\n"
        header += "Accept-Encoding: gzip, deflate\r\n"
        header += "Content-Type: application/x-www-form-urlencoded, application/json; charset=UTF-8\r\n"
        
        body = ''
        if args:
            for key in args:
                body += key+'='+args[key]+'&'
        body = body[:-1]+'\r\n'
        c_len = len(body)
        header += "Content-Length: "+str(c_len)+"\r\n"
        header += "Connection: keep-alive\r\n"
        header += "Upgrade-Insecure-Requests: 1\r\n"
        header += "DNT: 1\r\n"
        header += "\r\n"
        sock = self.connect(host, port)
        if not sock.sendall(header.encode()):
            data = self.recvall(sock)
            c, m, b = self.read_result(data)
            print("Log: ", c)
            return HTTPResponse(code=c, body=b)
        else:
            return ("Error in POST method")

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        ## running specified HTTP command
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        ## running GET command by default
        print(client.command( sys.argv[1] ))
