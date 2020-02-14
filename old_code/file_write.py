# Author: Amelia Rose
# Date: Jan 2020
# Description: Astro Pi Competition

import csv
import datetime


# Variables
FILENAME="astro_pi"
CURRENT_DATE_TIME = datetime.datetime.now()

# Test: Structure for data CSV
header = ['Temp', 'Humidity','Pressure', 'X', 'Y', 'Z']
test_line1 = ['20.2','44.7','1013.0','0','0','0']

# Write a comma separated file 
def createCSV(filename):
    with open(filename, mode='w') as astro_pi:
        astro_pi = csv.writer(astro_pi, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write data
        astro_pi.writerow(header);
        astro_pi.writerow(test_line1);

# Test: Create a filename
def createFilename():
    filename = CURRENT_DATE_TIME.strftime("%H%M%S") + "-" + CURRENT_DATE_TIME.strftime("%b") + "-" + FILENAME  
    return filename


# Run app
filename = createFilename()
createCSV(filename)
