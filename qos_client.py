# -*- coding: utf-8 -*-
from collections import Counter
import socket
import sys
import time
import threading
import commands

# cmd: python qos.py ip:port long $int short $int
# long $int for hold, short $int persecond
url = sys.argv[1].split(':')
req_type = {'long': int(sys.argv[3]), 'short':  int(sys.argv[5])}
socket.setdefaulttimeout(0.9)
ipvx = socket.AF_INET if '.' in url[0] else socket.AF_INET6

class QosClient:
    res = {'long': [], 'short': []}

    def __init__(self, url, req_type):
        self.url = url
        self.req_type = req_type
        self.req_line = "GET /%s HTTP/1.1\r\nHost:elb.cn\r\n\r\n" % req_type
    
    def req(self):
        try:
            soc = socket.socket(ipvx, socket.SOCK_STREAM)
            soc.connect((self.url[0], int(self.url[1])))
            soc.send(self.req_line)
            QosClient.res[self.req_type].append(0)
            if self.req_type == 'long':
                while True:
                    soc.send(self.req_line)
                    time.sleep(30)
            soc.shutdown(1)
        except Exception as err:
            print(err)


def output():
    short_tmp = len(QosClient.res['short'])
    while True:
        time.sleep(1)
        conn_pers, short_tmp = len(QosClient.res['short']) - short_tmp, len(QosClient.res['short'])
        state_list = commands.getstatusoutput("ss -4na | grep %s | awk '{print $2}'"% url[0])[1].split('\n')
        print('short: %d/s'%(conn_pers), Counter(state_list), 'active_thread: %d'% threading.active_count())
        if short_tmp > 100000:
            QosClient.res = {'long': [], 'short': []}

if __name__ == "__main__":
    print('req_type:', req_type, 'url:', url)

    log = threading.Thread(target=output)
    log.setDaemon(True)
    log.start()
    long_client = QosClient(url, "long")
    short_client = QosClient(url, "short")

    for _ in range(req_type['long']):
        t = threading.Thread(target=long_client.req)
        t.setDaemon(True)
        t.start()
    
    start_time = time.time()
    is_break = False
    while True:
        try:
            for _ in range(req_type['short']):
                threading.Thread(target=short_client.req).start()
            time.sleep(1)
        except KeyboardInterrupt:
            break
    print("\n=====speed: %d/s=====" % (len(QosClient.res['short']) / int(time.time() - start_time)))
