#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 20:09:35 2022

@author: parisp15
"""

# echo-client.py

import socket
import sys

sys.path.append('/opt/openrvdas/')


#224.0.0.251
#192.168.86.249

HOST = "127.0.0.1"  #"127.0.0.1"  # The server's hostname or IP address
PORT = 56432  #65432  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((HOST, PORT))


while True:
    s.send(b"Hello!")
    data = s.recv(1024) # buffer size is 1024 bytes

    print(data) 

   
# Start Server:  Can you insert a wait between record sends?
#/opt/openrvdas/logger/utils/simulate_network.py --port 65432 --filebase /Users/parisp15/Documents/NCSU/NMEA_strings.csv     --instrument Vector_GPS     --loop


# Start listener:  to work with a config file.
#logger/listener/listen.py --udp 56432 --write_file -