#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
echo_server.py

UDP server shipping NMEA sentences via openRVDAS's UDP_Writer, such that it
might be read by the corresponding UDP Reader in CSI_Listener.py or 
openRVDAS's Listen.py

The server reads an existing file of NMEA strings, comma sdparated values,
and writes these using a UDP_Writer instance to the specified port on the
local network. The port is provided by the user in the variable naed (aptly)
PORT.

As the name of the writer implies (well, it's pretty explicit actually) the
protocol is UDP

Created on Mon Dec 12 19:53:36 2022

to start the server enter the following on an idle command prompt:
    
    ./echo_server.py
    
    
to stop the server:
    
    Cntl-C
    
it's not graceful but it gets the job done...


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

DESTINATION = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 56432  # Port to listen/write on/to (non-privileged ports are > 1023)

try:
    # load NMEA sentences from source file into a Python list...
    print('loading NMEA sentences from source')
    
    f = open('./VectorHemisphere330_NMEA_sentence_stream','r')
except Exception as e:
    print('Problem opening the sentence source data...', e)

nmea_strings = []

with f:
    for line in f:
        nmea_strings.append(line)     # .encode("utf-8")
        
    f.close()
    

reader = UDPReader(port=PORT)
writer = UDPWriter(port=PORT)

print('Server up and running... \n and broadcasting...')

c = 0
repeats = 0

while c <= 5000:
   data_to_send = nmea_strings[c]

   wait_time = 1.0
   time.sleep(wait_time)        # wait wait_time sec between packets

   writer.write(data_to_send)   
   
   c = c + 1
   
   if c == 5000:
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
