#!/usr/bin/env python
# coding=utf-8
import socket
import argparse
import time
import SocketServer

parser = argparse.ArgumentParser(description='Manual to this tcp_server.py')
parser.add_argument('-6', '--ipv6', default=False, help="ipv6 Switch", action='store_true')
parser.add_argument('-p', '--port', type=int, help="server port")
args = parser.parse_args()

class MyServer(SocketServer.BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(1024)[:30]
            self.request.sendall(data)
            if data == '' or "short" in data:
                break
            time.sleep(1)
        self.request.close()

if __name__ == '__main__':
    if args.ipv6:
        SocketServer.TCPServer.address_family = socket.AF_INET6
    server = SocketServer.ThreadingTCPServer(('', args.port), MyServer)
    print("Start listening at %d" % args.port)
    server.serve_forever()
