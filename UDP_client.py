#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 14:26:12 2023

@author: parisp15
"""

import sys

sys.append.path('Users/parisp15/Documents/NCSU/')
import NMEA_Sentence_Parser_Functions as parsers


sys.path.append('/opt/openrvdas/')
from logger.readers.udp_reader import UDPReader

# writers:
from logger.writers.text_file_writer import TextFileWriter
from logger.writers.influxdb_writer import InfluxDBWriter
from logger.writers.udp_writer import UDPWriter


# $$$$$ Set Up Buckets in the influxDB for each sentence type $$$$$$$$$$$$$$$$$
#

def create_influx_buckets():
    '''
    Parameters: None

    Returns: Python list of pointers to influxDBWriter instances
    -------
    None.

    '''
    # set influxDB credentials:
    INFLUXDB_AUTH_TOKEN = 'MAulD3Xi-72yNaNzoHAMDeuWI4KK4Wd1dnLB9slc-y3srffMy1oFOYmJBAOMVF8KICtY8fvfg_btmTvVZTashA=='
    INFLUXDB_ORG = 'openrvdas'
    INFLUXDB_URL = 'http://localhost:8086'
    INFLUXDB_VERIFY_SSL = False

    # inflbuxDB bucket names
    buckets = ['hdt','vtg','gga','pashr']
    bucket_list = []

    for bucket in buckets:
        
        writer_id = bucket+'_writer'

        writer_id = InfluxDBWriter(bucket_name=bucket, \
                            measurement_name=bucket, \
                            auth_token=INFLUXDB_AUTH_TOKEN, \
                            org=INFLUXDB_ORG, \
                            url=INFLUXDB_URL, \
                            verify_ssl=INFLUXDB_VERIFY_SSL)
        
        bucket_list.append(writer_id)
        
    return(bucket_list)



# $$$$$ Instatntiate log file writer objects for each sentence type $$$$$$$$$$$
def create_logfile_writers():
    '''
    Parameters: None

    Returns: Python list of pointers to influxDBWriter instances
    -------
    None.
    
    NOT CURRENTLY USED! Replaced by create_log_file_writer()

    '''
    base_path = '/Users/parisp15/Documents/'
    extension = '_log.csv'
    
    # NMEA log file ids:
    log_file_ids = ['hdt','vtg','gga','pashr']
    log_writer_list = []

    for log_file_id in log_file_ids:
        
        text_writer = log_file_id+'_writer'
        log_file_path = base_path+log_file_id+extension
        
        text_writer = TextFileWriter(log_file_path)
        
        log_writer_list.append(text_writer)
        
    return(log_writer_list)

# Logfile_path = '/Users/parisp15/Documents/gyro_log.csv'



# $$$$$ Instatntiate log file writer object, one file for all talk ids $$$$$$$$$
def create_logfile_writer():
    '''
    Parameters: None

    Returns: pointer instance to influxDBWriter
    -------
    None.
    
   Replaces, for now, create_log_file_writers()

    '''
    base_path = '/Users/parisp15/Documents/'
    
    text_writer = TextFileWriter(base_path+'VectorHemisphere330_log.csv')
    
    return(text_writer)




 # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
 # 
 # Main Task Dispatch:
 #
 # 

# set a port to read from
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 56432  # Port to listen on (non-privileged ports are > 1023)

reader = UDPReader(PORT)

# create database buckets:
bucket_list = create_influx_buckets()
 
# instantiate log file writer instances:
log_file = create_logfile_writer()

print('running...')

record_counter = 0  

while True:
    print('Im here')
    try:
        data = reader.read()
        
        dl = data.decode("utf-8").split(',')    # convert bytes to str then to list
    except Exception as e:
         print('Something went wrong...',e)
         

  
    log_file.write(data+time_stamp)   # .decode("utf-8")
    
    print(data)
    
    

    data = reader.read() 
    
    # trac k and report number of sentences processed..
    record_counter = record_counter + 1
        
    if record_counter % 50 == 0:
        print(record_counter, 'records processed...'
    

             