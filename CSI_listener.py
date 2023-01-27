#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 22:56:16 2023

The model / example upon which everything was built:
# parser = RecordParser(
#                  record_format='{data_id:w} {timestamp:ti} {field_string}',
#                  field_patterns=[
#                    '{:d}:{GravityValue:d} {GravityError:d}']
#                )
 
# p = parser.parse_record('grv1 2017-11-10T01:00:06.572Z 01:024557 00')

# print(p)
# output: {'data_id': 'grv1', 'timestamp': 1510275606.572, 'fields': {'GravityValue': 24557, 'GravityError': 0}}


@author: parisp15
"""

import sys
from datetime import datetime

logfile_path = '/Users/parisp15/Documents/'
sys.path.append('/opt/openrvdas/')
sys.path.append('Users/parisp15/Documents/GitHub/openrvdas_ui/')

import NMEA_sentence_parsing_definitions as NMEA_parsers

# readers:
from logger.readers.udp_reader import UDPReader

# transforms:
# from logger.transforms.parse_transform import ParseTransform
from logger.transforms.timestamp_transform import TimestampTransform
#from logger.transforms.to_das_record_transform import ToDASRecordTransform
from logger.transforms.prefix_transform import PrefixTransform

# writers:
from logger.writers.text_file_writer import TextFileWriter
from logger.writers.logfile_writer import LogfileWriter
from logger.writers.influxdb_writer import InfluxDBWriter
from logger.writers.udp_writer import UDPWriter

from logger.utils.record_parser import RecordParser




# $$$$$ Set Up Buckets in the influxDB for each sentence type $$$$$$$$$$$$$$$$$

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




    
# $$$$$ For HDT $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$





# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 
# Main Task Dispatch:
#
# 
#224.0.0.251
#192.168.86.249  # the Ms Caroline's network, perhaps?

HOST = "192.168.1.255"  # <-- suggested static IP addr if DHCP not available
PORT = 56432  # 16003 <--Miss Caroline's VectorHemi330
BROADCAST_PORT = 65432

# instantiate reader, transform, and writer instances: 
data_reader = UDPReader(PORT)

timestamp = TimestampTransform(sep=',')
prefix = PrefixTransform('vh300')

date_of_today = datetime.utcnow().strftime('%Y-%m-%d')
log_writer = LogfileWriter(logfile_path+'VectorHemisphere330_log')
text_writer = TextFileWriter(logfile_path+'VectorHemisphere330_log_csv-'+date_of_today)

udp_writer = UDPWriter(BROADCAST_PORT)


# create databsase buckets:
bucket_list = create_influx_buckets()


# LET'S GET STARTED...
print('running...')
record_counter = 0

while True:

    data = data_reader.read()

    try:
        dl = data.split(',')    # convert bytes to str then to list decode("utf-8")
    except Exception as e:
        print('Something went wrong trying to split the raw data stream...',e)
     
    try:    
        if dl[0] == '$GPHDT':
            das_record = NMEA_parsers.handle_hdt_sentences(data)
            bucket_list[0].write(das_record)
        
        if dl[0] == '$GPVTG':
            das_record = NMEA_parsers.handle_vtg_sentences(data)
            bucket_list[1].write(das_record)
        
        if dl[0] == '$PASHR':
            das_record = NMEA_parsers.handle_pashr_sentences(data)
            bucket_list[3].write(das_record)
        
        if dl[0] == '$GPGGA':
            das_record = NMEA_parsers.handle_gga_sentences(data)   #.decode("utf-8")
            bucket_list[2].write(das_record)
    except Exception as e:
        print('Sentence parsing error:', e)
        
        
    # returns time stamp from DAS Record in UNIX seconds...
    time_stamp = ','+str(das_record['timestamp'])

    # TimestampTransform returns ISO 8601 time
    log_writer.write(TimestampTransform().transform(data))
    text_writer.write(data.rstrip()+time_stamp)
    
    # write data unaltered back out onto the network:    
    udp_writer.write(data)
    
   
    # trac k and report number of sentences processed..
    record_counter = record_counter + 1
        
    if record_counter % 50 == 0:
        print(record_counter, 'records processed...')
        