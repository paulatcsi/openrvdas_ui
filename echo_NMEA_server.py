#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 19:53:36 2022

@author: parisp15
"""

# echo-server.py


nmea_strings=[b'$GPGGA,191119.90,3552.52780014,N,07539.67962499,W,2,08,1.0,-1.358,M,-36.497,M,4.9,0131*51',
b'$GPHDT,259.816,T*34',
b'$GPVTG,93.84,T,104.94,M,0.04,N,0.07,K,D*1B',
b'$PASHR,191119.00,260.12,T,0.01,-4.18,-0.01,0.179,0.527,0.117,1*3F',
b'$GPVTG,172.52,T,183.62,M,0.02,N,0.04,K,D*2D',
b'$GPHDT,259.445,T*3E',
b'$GPGGA,191121.10,3552.52780223,N,07539.67961630,W,2,08,1.0,-1.357,M,-36.497,M,6.1,0131*53',
b'$PASHR,191121.00,259.50,T,0.04,-4.40,-0.01,0.177,0.556,0.116,1*39',
b'$GPHDT,259.581,T*37',
b'$GPGGA,191122.30,3552.52780841,N,07539.67962105,W,2,08,1.0,-1.358,M,-36.497,M,7.3,0131*52',
b'$GPVTG,133.80,T,144.91,M,0.01,N,0.02,K,D*25',
b'$PASHR,191122.00,259.52,T,-0.04,-4.21,-0.01,0.174,0.591,0.114,1*18',
b'$GPHDT,259.814,T*36',
b'$GPGGA,191123.50,3552.52781377,N,07539.67962966,W,2,08,1.0,-1.356,M,-36.497,M,7.5,0131*5F',
b'$GPVTG,7.13,T,18.23,M,0.03,N,0.06,K,D*1E',
b'$PASHR,191123.00,259.72,T,0.14,-4.31,-0.01,0.174,0.580,0.114,1*36']


import socket
import time
import sys


# load NMEA sentences from source file into a Python list...
print('loading NMEA ssentences from source')

f = open('simulated_nmea_sentences.csv','r')

nmea_strings = []

with f:
    for line in f:
        nmea_strings.append(line)
        
f.close()
        

# open a port and socket and go to it
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 56432        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))


print("Connected. Server up and running... \n and listening...")

c = 0
while c <= 431:
   data, addr  = s.recvfrom(1024)
   data_to_send = nmea_strings[c].encode("utf-8")
   s.sendto(data_to_send, addr)
   
   #writer.write(data_to_send)
   
   #s.sendto(data_to_send, (HOST,PORT))
   
   time.sleep(0.5)                   # wait 1 sec betwen packets
   if c == 431:
        c = 0
   else:
        c = c + 1
                

s.close()




#  # closing an open port:  sudo kill -9 $(lsof -t -i:8080)
 
#   # Let's send data through UDP protocol
# while True:
#     send_data = input("Type some text to send =>");
#     s.sendto(send_data.encode('utf-8'), (ip, port))
#     print("\n\n 1. Client Sent : ", send_data, "\n\n")
#     data, address = s.recvfrom(4096)
#     print("\n\n 2. Client received : ", data.decode('utf-8'), "\n\n")
# # close the socket
# s.close()