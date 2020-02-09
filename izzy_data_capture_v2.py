#!/usr/bin/python
from sense_hat import SenseHat
import time
import sys
import datetime
import ephem


IZ_line1 = "1 25544U 98067A   20039.12879017  .00000424  00000-0  15820-4 0  9999"
IZ_line2 = "2 25544  51.6447 271.9826 0004963 240.2524 269.3653 15.49145717211850"

station_name = "ISS (ZARYA)"

sense = SenseHat()
sense.clear()

IZ_Temp = IZ_Humid = IZ_Presh = 0.0
IZ_Lat = 0.0
IZ_Long = 0.0



def get_temp(Temp):
    
        Temp = sense.get_temperature()
        Temp = round(Temp, 1)
        return (Temp)

def get_humidity(Humid):
    
        Humid = sense.get_humidity()  
        Humid = round(Humid, 1)  
        return (Humid)

def get_pressure(Presh):

        Presh = sense.get_pressure()
        Presh = round(Presh, 1)
        return (Presh)

def get_iss_long(station_name, IZ_Long, IZ_line1, IZ_line2):
    
    l1 = IZ_line1
    l2 = IZ_line2
    iss = ephem.readtle(station_name, l1, l2)

    iss.compute()
    long_value = [float(i) for i in str(iss.sublong).split(":")]
    return (long_value)

def get_iss_lat(station_name, IZ_Lat, IZ_line1, IZ_line2):

    l1 = IZ_line1
    l2 = IZ_line2
    iss = ephem.readtle(station_name, l1, l2)

    iss.compute()
    lat_value = [float(i) for i in str(iss.sublat).split(":")]
    return (lat_value)

def output_data(Temp, Humid, Presh, IZ_Long, IZ_Lat):

        # print("Longitude: " str(IZ_Long))
        # print("Latitude: " str(IZ_Lat))
        print (time.strftime('%x %X'),Temp, Humid, Presh, str(IZ_Long), str(IZ_Lat))
       
        return


try:
      while True:
            IZ_Temp = get_temp(IZ_Temp)
            IZ_Humid = get_humidity(IZ_Humid)
            IZ_Presh = get_pressure(IZ_Presh)
            IZ_Long = get_iss_long(station_name, IZ_Long, IZ_line1, IZ_line2)
            IZ_Lat = get_iss_lat(station_name, IZ_Lat, IZ_line1, IZ_line2)
            output_data(IZ_Temp, IZ_Humid, IZ_Presh, IZ_Long, IZ_Lat)
     
            time.sleep(30)
except KeyboardInterrupt:
      pass

