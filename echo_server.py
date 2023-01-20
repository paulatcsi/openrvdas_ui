#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
echo_server.py

UDP server shipping NMEA strings via openRVDAS's UDP_Writer, such that it
might be read by the corresponding UDP REader in Listen.py

hoping...

Created on Mon Dec 12 19:53:36 2022

to start the server enter the following on an idle command prompt:
    
    ./echo_server.py
    
    
to stop the server:
    
    Cntl-C


if it becomes necessary to force "close" the port, enter the following at a
command prompt:
    
    sudo kill -9 $(lsof -t -i:56432)
    
@author: parisp15
"""

#import socket
import sys
import time

sys.path.append('/opt/openrvdas/')
from logger.writers.udp_writer import UDPWriter
from logger.readers.udp_reader import UDPReader

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 56432  # Port to listen on (non-privileged ports are > 1023)


# load NMEA sentences from source file into a Python list...
print('loading NMEA sentences from source')

f = open('simulated_nmea_sentences.csv','r')

nmea_strings = []

with f:
    for line in f:
        nmea_strings.append(line)     # .encode("utf-8")
        
    f.close()
    

reader = UDPReader(port=PORT)
writer = UDPWriter(port=PORT)

print('Server up and running... \n and listening...')

c = 0
repeats = 0

while c <= 431:
   data_to_send = nmea_strings[c]
   
   wait_time = 1.0
   time.sleep(wait_time)        # wait wait_time sec between packets
   
   writer.write(data_to_send)   
   
   c = c + 1
   
   if c == 431:
        c = 0
        repeats = repeats + 1
        
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)