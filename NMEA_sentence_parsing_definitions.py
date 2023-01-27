#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NMEA_sentence_parsing_definitions.py

functions holding the sentence parsing definitions for NMEA sentence strings
handled by the CSI_listener.py script. At the initial writing the sentences:
    - HDT
    - GGA
    - VDT
    - PASHR (not actually an NMEA sentence but we handle it anyway)
    
    
This file is a Python Module that is meant to be imported by CSI_Listener.py
and is called by the main task dispatch section of that sript to handle the
parsing duties for data captured from one or more various on-shipboard
instruments for archive, on-the-fly analysis, display, etc.

Defintion functions can be added as the sentence handling repertoire expands

NOTE: this file should remain a peer to the script CSI_listener.py for ease of
use--in fact, CSI_listener.py expects to "see" this module file in the same
sub-folder as itself. If not, you'll have to either move a copy of this file
to the subdir where CSI)listener.py is located, or alter the search path in
    CSI_listener so that the latter can find and load it
    
    
Created on Tue Jan 24 16:06:50 2023

@author: parisp15
"""

import sys

sys.path.append('/opt/openrvdas/')
sys.path.append('Users/parisp15/Documents/GitHub/openrvdas_ui/')


# transforms:
from logger.transforms.timestamp_transform import TimestampTransform

from logger.utils.record_parser import RecordParser



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


