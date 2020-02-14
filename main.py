# Author: Team Izzy (Kya, Kwame, Amelia)
# Date: Jan 2020
# Description: Astro Pi Competition

import csv
import sys
import time
import ephem
import datetime
from sense_hat import SenseHat
#from picamera import PiCamera

# Sense Hat 
sense = SenseHat()
sense.clear()

# Pi Camera
# camera = PiCamera
# camera.resolution(1920, 1080)
# camera.start_preview()

# Variables
## PROD
#LAB_MAX_DURATION = (60 * 3)
#LAB_SLEEP = 30
#LAB_IMAGE_DELAY = 5

## TEST
LAB_MAX_DURATION = 2
LAB_SLEEP = 2
LAB_IMAGE_DELAY = 1
IZ_line1 = "1 25544U 98067A   20039.12879017  .00000424  00000-0  15820-4 0  9999"
IZ_line2 = "2 25544  51.6447 271.9826 0004963 240.2524 269.3653 15.49145717211850"
station_name = "ISS (ZARYA)"

LAB_PRECISION = 2
FILENAME="astro_pi"
TXT_EXT=".txt"
IMG_EXT=".jpg"
index = 0
IZ_Temp = IZ_Humid = IZ_Presh = 0.0
IZ_Lat = 0.0
IZ_Long = 0.0


header = ['Temp', 'Humidity','Pressure', 'X', 'Y', 'Z']
test_line1 = ['20.2','44.7','1013.0','0','0','0']

################
# PI CAMERA

def get_Image(filename):
   print("Taking a picture")
   # Capture(filename)

def tag_Image():
    # Call get iss long
    # Call get iss lat
    # Use EXIF to tag the Image with coordinates



################
# SENSE HAT

def get_temp():
    
        Temp = sense.get_temperature()
        Temp = round(Temp, LAB_PRECISION)
        return (Temp)

def get_humidity():
    
        Humid = sense.get_humidity()  
        Humid = round(Humid, LAB_PRECISION)  
        return (Humid)

def get_pressure():

        Presh = sense.get_pressure()
        Presh = round(Presh, LAB_PRECISION)
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


def get_accelerometer():
  acceleration = sense.get_accelerometer_raw()
  x = round(acceleration['x'], LAB_PRECISION)
  y = round(acceleration['y'], LAB_PRECISION)
  z = round(acceleration['z'], LAB_PRECISION)

  return x, y, z

# Format
# header = ['Temp', 'Humidity','Pressure', 'X', 'Y', 'Z']
# test_line1 = ['20.2','44.7','1013.0','0','0','0']


def output_data(Temp, Humid, Presh, IZ_Long, IZ_Lat):

    # print("Longitude: " str(IZ_Long))
    # print("Latitude: " str(IZ_Lat))
    # print (time.strftime('%x %X'),Temp, Humid, Presh, str(IZ_Long), str(IZ_Lat))
    print (time.strftime('%x %X'),Temp, Humid, Presh,)      
    return


################
# File Management


# Name: createCSV 
# Description: Write a CSV file with header and data

def piCamera(filename):
    print ("piCamera: " + filename )

def piSenseHat(filename):
    print ("piSenseHat: " + filename)
    temp = get_temp()
    humidity = get_humidity()
    pressure = get_pressure()
    x, y, z = get_accelerometer()
    
    print (str(get_temp()) + "," + str(get_humidity()) + "," + str(get_pressure()) + "," + str(x) + "," + str(y) + "," + str(z))
    data=[str(get_temp()) + "," + str(get_humidity()) + "," + str(get_pressure()) + "," + str(x) + "," + str(y) + "," + str(z)]
    createCSV(filename, data)


def createCSV(filename, data):
    with open(filename, mode='w') as astro_pi:
        astro_pi = csv.writer(astro_pi, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       
        astro_pi.writerow(header);
        astro_pi.writerow(test_line1);


# Name: createFilename
# Description: Create a filename based on current date + string
def createFilename(index):
    filename = ""
    CURRENT_DATE_TIME = datetime.datetime.now()
    filename = str(index) + "-" + CURRENT_DATE_TIME.strftime("%H%M%S") + "-" + CURRENT_DATE_TIME.strftime("%b") + "-" + FILENAME
    return filename



################
# Utility 
def getLaunchTime():
  return datetime.datetime.now()

def getTimeDifference(startTime, minutesToAdd):
  return startTime + datetime.timedelta(minutes=minutesToAdd)

def getDebug():
  print ("")
  print ("-----------------------------------------")
  print ("Debug:")
  print ("-----------------------------------------")
  print ("Camera delay: " + str(imageCaptureDelay))
  print ("Lab Duration: " + str(timeCompletion))
  print ("Time now: " + str(timeNow))
  print ("-----------------------------------------")
  print ("")

################
# Main Program

# Call Time functions
timeLaunched = getLaunchTime()
timeCompletion = getTimeDifference(timeLaunched, LAB_MAX_DURATION)
imageCaptureDelay = getTimeDifference(timeLaunched, LAB_IMAGE_DELAY)


# Perform Lab tasks
while True:

  # Save the current time
  timeNow = datetime.datetime.now()

  # Get a unique filename
  filename = createFilename(index)
  
  # Call Gather SenseHat data
  piSenseHat(filename + TXT_EXT)

  if (timeNow >= imageCaptureDelay):
    # Call to capture image
    piCamera(filename + IMG_EXT)

    # Reset the camera delay - based on current time
    imageCaptureDelay = getTimeDifference(timeNow, LAB_IMAGE_DELAY)

  # Index filenames
  index = index + 1

  # Check Lab duration 
  if (timeNow >= timeCompletion):
    break

  # Pause the lab
  time.sleep(LAB_SLEEP)
  getDebug()


