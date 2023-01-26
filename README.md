# openrvdas_ui
Underway user interface for onboard GNSS, R/V Robertson


Repo contains the base data capture code and yaml configuration files for R/V Robertson cruises.

- script echo_server.py provides a simulated UDP data stream which can be read by openRVDAS's UDPReader via Listen.py or a home-grown listner script. The data strem consists of a loop-back of 471 (I think) NMEA sentences of type GGA, VDT, and H... A PASHR sentence is also included. Sentences are sent as text (not bytes!)



Notes:
 1.) The openRVDAS LogFile_Writer creates a text file with Windows line endings (x0Ax0D) which results in an empty line inserted between each logged data line. These Regex patterns can be used (in VIM for instance) to remove the extra lines:
 
 g/^$/d   or  g/^\n/d
 
 to remove the residual MS Windows carriage returns from the file:
 
 %s/\r//g
 
 to undo anything you've done in VIM press the lower case u key
 