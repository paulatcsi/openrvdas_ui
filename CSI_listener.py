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
import time

logfile_path = '/Users/parisp15/Documents/'
sys.path.append('/opt/openrvdas/')

# readera:
from logger.readers.udp_reader import UDPReader

# transforms:
# from logger.transforms.parse_transform import ParseTransform
from logger.transforms.timestamp_transform import TimestampTransform
from logger.transforms.to_das_record_transform import ToDASRecordTransform
from logger.transforms.prefix_transform import PrefixTransform

# writers:
from logger.writers.text_file_writer import TextFileWriter
from logger.writers.logfile_writer import LogfileWriter
from logger.writers.influxdb_writer import InfluxDBWriter

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

def handle_hdt_sentences(nmea_sentence):
    '''
    Parameters
    ----------
    nmea_sentence: TYPE
        DESCRIPTION.

    Returns
    -------
    A Python dictionary formatted as a DASRecord.
    
    nmea_sentence = '$GPHDT,259.816,T*34'

    '''
    
    #toDASRec = ToDASRecordTransform('GPHDT')

    # add the timestamp...
    nmea_sentence = TimestampTransform(sep=',').transform(nmea_sentence)      # {timestamp:ti},

    parser = RecordParser(
                  record_format='{timestamp:ti},{data_id:nc},{field_string}',
                  field_patterns=['{HeadingTrue:g},{mode:w}*{CheckSum:x}'],
                  delimiter=','
                    )

    das_record = parser.parse_record(nmea_sentence)
    #das_record = toDASRec.transform(p)
    #print('For HDT:','\n',p,'\n')
    
    return(das_record)



# $$$$$ For GGA $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def handle_gga_sentences(nmea_sentence):
    '''
    Parameters
    ----------
    nmea_sentence: TYPE
        DESCRIPTION.

    Returns
    -------
    A Python dictionary formatted as a DASRecord.
    
    
    nmea_sentence = '$GPGGA,191119.90,3552.52780014,N,07539.67962499,W,2,08,1.0,-1.358,M,-36.497,M,4.9,0131*51'
    '''           

    format_definition = '{Time:f},{Latitude:nlat},{NorS:w},{Longitude:nlat},'
    format_definition = format_definition + '{EorW:w},{FixQuality:d},{NumSats:d},{HDOP:of},'
    format_definition = format_definition + '{AntennaHeight:of},{AntHt_units:w},'
    format_definition = format_definition + '{GeoidHeight:of},{GeoHt_units:w},{LastDGPSUpdate:of},'
    format_definition = format_definition + '{DGPSStationID:od}*{CheckSum:x}'

    # add the timestamp...
    nmea_sentence = TimestampTransform(sep=',').transform(nmea_sentence)
    #toDASRec = ToDASRecordTransform('GPGGA')

    parser = RecordParser(
                  record_format='{timestamp:ti},{data_id:nc},{field_string}',
                  field_patterns=[format_definition],
                  delimiter=','
                    )

    das_record = parser.parse_record(nmea_sentence)
    #das_record = toDASRec.transform(p)
    #print('For GGA:','\n',p,'\n')

    return(das_record)

# $$$$$ For VTG $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def handle_vtg_sentences(nmea_sentence):
    '''
    Parameters
    ----------
    nmea_sentence: TYPE
        DESCRIPTION.

    Returns
    -------
    A Python dictionary formatted as a DASRecord.
    
    nmea_sentence = '$GPVTG,93.84,T,104.94,M,0.04,N,0.07,K,D*1B'
    '''           

    format_definition = '{TrackMG_True:f},{TrackMG_T:w},{TrackMG_Mag:f},{TrackMG_M:w},'
    format_definition = format_definition + '{GndSpd_Knots:f},{GndSpd_K:w},'
    format_definition = format_definition + '{GndSpd_KiloPHr:f},{GndSpd_KPH:w},'
    format_definition = format_definition + '{mode:w}*{CheckSum:x}'

    # add the timestamp...
    nmea_sentence = TimestampTransform(sep=',').transform(nmea_sentence)
    #toDASRec = ToDASRecordTransform('GPVTG')

    parser = RecordParser(
                  record_format='{timestamp:ti},{data_id:nc},{field_string}',
                  field_patterns=[format_definition],
                  delimiter=','
                    )

    das_record = parser.parse_record(nmea_sentence)
    #das_record = toDASRec.transform(p)
    #print('For VTG:','\n',p,'\n')
    
    return(das_record)


# $$$$$ For PASHR $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def handle_pashr_sentences(nmea_sentence):
    '''
    Parameters
    ----------
    nmea_sentence: TYPE
        DESCRIPTION.

    Returns
    -------
    A Python dictionary formatted as a DASRecord.
    
    nmea_sentence = '$PASHR,191119.00,260.12,T,0.01,-4.18,-0.01,0.179,0.527,0.117,1*3F'
    '''           

    format_definition = '{Time:f},{Heading:f},{True_Hdg:w},{Roll:f},{pitch:f},'
    format_definition = format_definition + '{heave:f},{roll_sd:f},{pitch_sd:f}'
    format_definition = format_definition + ',{hdg_sd:f},{quality_flag:w}*{Checksum:x}'

    # add the timestamp...
    nmea_sentence = TimestampTransform(sep=',').transform(nmea_sentence)
    #toDASRec = ToDASRecordTransform('PASHR')

    parser = RecordParser(
                  record_format='{timestamp:ti},{data_id:nc},{field_string}',
                  field_patterns=[format_definition],
                  delimiter=','
                    )

    das_record = parser.parse_record(nmea_sentence)
    #das_record = toDASRec.transform(p)
    #print('For PASHR:','\n',das_record,'\n')

    return(das_record)



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 
# Main Task Dispatch:
#
# 
#224.0.0.251
#192.168.86.249  # the Ms Caroline's network, perhaps?

HOST = "127.0.0.1"  #"127.0.0.1"  # The server's hostname or IP address
PORT = 56432  #65432  # The port used by the server

# instantiate reader, transform, and writer instances: 
data_reader = UDPReader(PORT)

timestamp = TimestampTransform(sep=',')
prefix = PrefixTransform('vh300')

log_writer = LogfileWriter(logfile_path+'VectorHemisphere330_log')
text_writer = TextFileWriter(logfile_path+'VectorHemisphere330_log_txt')


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
        print('Something went wrong...',e)
        
    if dl[0] == '$GPHDT':
        das_record = handle_hdt_sentences(data)
        bucket_list[0].write(das_record)
        
    if dl[0] == '$GPVTG':
        das_record = handle_vtg_sentences(data)
        bucket_list[1].write(das_record)
        
    if dl[0] == '$PASHR':
        das_record = handle_pashr_sentences(data)
        bucket_list[3].write(das_record)
        
    if dl[0] == '$GPGGA':
        das_record = handle_gga_sentences(data)   #.decode("utf-8")
        bucket_list[2].write(das_record)
 
    # returns time stamp from DAS Record in UNIX seconds...
    time_stamp = ','+str(das_record['timestamp'])

    # TimestampTransform returns ISO 8601 time
    log_writer.write(TimestampTransform().transform(data))
    text_writer.write(data.rstrip()+time_stamp)
        
   
    # trac k and report number of sentences processed..
    record_counter = record_counter + 1
        
    if record_counter % 50 == 0:
        print(record_counter, 'records processed...')
        