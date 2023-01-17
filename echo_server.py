#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UDP server shipping NMEA strings via openRVDAS's UDP_Writer, such that it
might be read by the corresponding UDP REader in Listen.py

hoping...

Created on Mon Dec 12 19:53:36 2022

@author: parisp15
"""

# echo-server.py

#import socket
import sys
import time

sys.path.append('/opt/openrvdas/')
from logger.writers.udp_writer import UDPWriter
from logger.readers.udp_reader import UDPReader


# open a port and socket and go to it
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 56432  # Port to listen on (non-privileged ports are > 1023)


# load NMEA sentences from source file into a Python list...
print('loading NMEA ssentences from source')

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
   time.sleep(wait_time)        # wait wait_time sec betwen packets
   
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