# Authors: Amelia Rose, Kwame Williams, Kya Browne
# Date: Jan 2020
# Description: Astro Pi Mission Space Lab - Life on Eearth

import os
import csv
import datetime
from logzero import logger

from ephem import readtle, degree
from sense_hat import SenseHat
from picamera import PiCamera


def get_temp():
    temp = sense_hat.get_temperature()
    temp = round(temp, 2)
    return temp


def get_humidity():
    humid = sense_hat.get_humidity()
    humid = round(humid, 2)
    return humid


def get_pressure():
    pressure = sense_hat.get_pressure()
    pressure = round(pressure, 2)
    return pressure


def get_magnetic_field():
    pass # **** Kwame's Code to go here ****


def get_iss_longitude():
    iss.compute()

    longitude = [float(i) for i in str(iss.sublong).split(':')]

    if longitude[0] < 0:
        longitude[0] = abs(longitude[0])
        camera.exif_tags['GPS.GPSLongitudeRef'] = "W"
    else:
        camera.exif_tags['GPS.GPSLongitudeRef'] = "E"

    camera.exif_tags['GPS.GPSLongitude'] = '%d/1,%d/1,%d/10' % (longitude[0], longitude[1], longitude[2]*10)

    return iss.sublong / degree


def get_iss_latitude():
    iss.compute()

    latitude = [float(i) for i in str(iss.sublat).split(':')]

    if latitude[0] < 0:
        latitude[0] = abs(latitude[0])
        camera.exif_tags['GPS.GPSLatitudeRef'] = "S"
    else:
        camera.exif_tags['GPS.GPSLatitudeRef'] = "N"

    camera.exif_tags['GPS.GPSLatitude'] = '%d/1,%d/1,%d/10' % (latitude[0], latitude[1], latitude[2]*10)

    return iss.sublat / degree


def create_data_file():
    with open(data_file, mode='w') as astro_pi:
        astro_pi_writer = csv.writer(astro_pi, delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
        # Write data
        astro_pi_writer.writerow(csv_header)


def write_data_to_file():
    with open(data_file, 'a') as astro_pi:
        astro_pi_writer = csv.writer(astro_pi, delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
        astro_pi_writer.writerow(data)


def take_photo():
    pass  # **** Kya's Code to go Here ****


# First thing - find out when program started running
start_time = datetime.datetime.utcnow()

# Initial setup - filenames, logger, ISS location object, as well as
# SenseHAT and PiCam connection
dir_path = os.path.dirname(os.path.realpath(__file__))
log_file = dir_path + '/projectizzy_log.log'
data_file = dir_path + '/projectizzy_data.csv'
photo_file = dir_path + '/projectizzy_photo_'
logger.logfile(log_file)
logger.info('{} - Program Begin'.format(datetime.datetime.utcnow()))

station_name = "ISS (ZARYA)"
tle_l1 = "1 25544U 98067A 20039.12879017 .00000424 00000-0 15820-4 0 9999"
tle_l2 = "2 25544 51.6447 271.9826 0004963 240.2524 269.3653 15.49145717211850"
iss = readtle(station_name, tle_l1, tle_l2)
logger.info('{} - ISS TLE Initialised'.format(datetime.datetime.utcnow()))

sense_hat = SenseHat()
logger.info('{} - Connected to SenseHAT'.format(datetime.datetime.utcnow()))

camera = PiCamera()
camera.resolution(1920, 1080)
camera.start_preview()
photo_counter = 1
picture_interval_mins = 5
logger.info('{} - Connected to PiCam NoIR'.format(datetime.datetime.utcnow()))

csv_header = ['Date/Time', 'Temp', 'Humidity', 'Pressure', 'Magnetic_X',
              'Magnetic_Y', 'Magnetic_Z']

try:
    create_data_file()
except Exception as e:
    logger.error('{}: {})'.format(e.__class__.__name__, e))
else:
    logger.info('{} - Data file created successfully'.format(datetime.datetime.utcnow()))

logger.info('{} - Init complete, main programme starting'.format(datetime.datetime.utcnow()))
now_time = datetime.datetime.utcnow()

while (now_time < start_time + datetime.timedelta(minutes=175)):
    try:
        # Main program - take environment data every iteration. Take a photo
        # every five minutes
        pass # **** Main body of Code to go here with 30s interval ****
    except Exception as e:
        logger.error('{}: {})'.format(e.__class__.__name__, e))

camera.close()
logger.info('{} - Program end'.format(datetime.datetime.utcnow()))
