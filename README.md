# openrvdas_ui
Underway user interface for onboard GNSS, R/V Robertson


Repo contains the base data capture code and yaml configuration files for R/V Robertson cruises.

- script echo_server.py provides a simulated UDP data stream which can be read by openRVDAS's UDPReader via Listen.py or a home-grown listner script. The data strem consists of a loop-back of 471 (I think) NMEA sentences of type GGA, VDT, and H... A PASHR sentence is also included. Sentences are sent as text (not bytes!)
