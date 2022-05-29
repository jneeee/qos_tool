# qos tool

used for check Long link retention capability and Short connection concurrency capability

## usage

- qos_server.py
  `python qos_server.py -p 1000`
  - `-6` enable ipv6
  - `-p PORT` listen PORT
- qos_client.py:
  `python qos_client.py ip:port long $int short $int`
  long $int for hold, short $int persecond
