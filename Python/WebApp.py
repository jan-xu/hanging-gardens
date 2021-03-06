'''

University of California, Berkeley
CE 186 Design of Cyber-Physical Systems (Fall Term 2018)
Hanging Gardens: WebApp.py
Group 6

Web application

'''

# Import required modules
import serial
import time
import requests
import json
import datetime
import pytz
from tzlocal import get_localzone
from DataAnalysis import analysis, time_reset, illuminance_calc
from ServerRequests import create_object, create_stream, update_point, get_exposure

# Change the port name to match the port to which Arduino is connected
#serial_port_name = '/dev/cu.usbmodem144401' # for Mac
serial_port_name = '/dev/cu.usbserial-DN01J2G2' # for Mac
ser = serial.Serial(serial_port_name, 9600, timeout=1)
time.sleep(5)

# Set up network details
base = 'http://127.0.0.1:5000'

object_names = {
    # Raw data
    -1:  'Light Sensor',
    -2:  'Light Sensor',
    -3:  'Light Sensor',
    -4:  'Water Lever Meter',
    -5:  'Water Lever Meter',
    -6:  'Thermometer',

    # Processed data
    -7:  'Exposure',
    -8:  'Energy Consumption',
    -9:  'Energy Consumption',
    -10: 'Energy Consumption',
    -11: 'Energy Consumption'
}

object_tags = {
    # Raw data
    -1:  'light_sensor',
    -2:  'light_sensor',
    -3:  'light_sensor',
    -4:  'water_level_meter',
    -5:  'water_level_meter',
    -6:  'thermometer',

    # Processed data
    -7:  'exposure',
    -8:  'energy',
    -9:  'energy',
    -10: 'energy',
    -11: 'energy'
}

points_type = { # 'i', 'f', or 's'
    # Raw data
    -1:  'i',
    -2:  'i',
    -3:  'i',
    -4:  'i',
    -5:  'i',
    -6:  'f',

    # Processed data
    -7:  'f',
    -8:  'f',
    -9:  'f',
    -10: 'f',
    -11: 'f'
}

stream_names = {
    # Raw data
    -1:  'Left Light Sensor',
    -2:  'Right Light Sensor',
    -3:  'Center Light Sensor',
    -4:  'Lower Water Level',
    -5:  'Upper Water Level',
    -6:  'Temperature',

    # Processed data
    -7:  'Daily light exposure',
    -8:  'LED',
    -9:  'Pump',
    -10: 'Valves',
    -11: 'Total energy consumption'
}

stream_tags = {
    # Raw data
    -1:  'left_light',
    -2:  'right_light',
    -3:  'center_light',
    -4:  'lower_water_level',
    -5:  'upper_water_level',
    -6:  'temperature',

    # Processed data
    -7:  'exposure',
    -8:  'led_power',
    -9:  'pump_power',
    -10: 'valve_power',
    -11: 'total_energy'
}

act_tags = {
    'roof': 'a',
    'flush': 'b',
    'LED': 'c'
}

act_state_tags = {
    -101: 'vlwr',
    -102: 'vupr',
    -103: 'pump'
}

# Define setup function that runs once at the start
def setup():
    try:
        print "Setup"
        print ""

        for i in range(-11,0):
            # Create objects and streams if not existing
            create_object(object_names[i], object_tags[i], base)
            create_stream(stream_names[i], points_type[i], object_tags[i], stream_tags[i], base)

        # Initialize setup time
        start_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        # Initialize reset time for exposure
        exp_reset_time = time_reset(datetime.datetime.now())

        # Initialize today's reset time for exposure count
        exp_reset_time_today = time_reset(datetime.datetime.now() - datetime.timedelta(1))

        # Initialize exposure count
        exposure = get_exposure(exp_reset_time_today, base, error=False)

        return start_time, exp_reset_time, exposure
    except:
        print "Setup Error"
        print ""

# Define setup function that runs continuously forever
def loop(time_last_flush, exp_reset_time, exposure):
    # Define current time
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    # Set exposure to zero if time is past 7 AM, and find new reset time
    if now >= exp_reset_time:
        exposure = 0
        exp_reset_time = time_reset(datetime.datetime.now())

    # Check if something is in serial buffer
    if ser.inWaiting() > 0:
        i = int(ser.readline()) # attributes i with the sensor data tag
        if i >= -100 and i < 0: # all sensor tags are negative integers between -100 (really -6) and -1
            try:
                # Read entire line for data point (subject to data type)
                if points_type[i] == 'i':
                    x = int(ser.readline())
                elif points_type[i] == 'f':
                    x = float(ser.readline())

                # Print info of the data point
                print "Time:", now.astimezone(get_localzone()).strftime("%Y-%m-%d %H:%M:%S")
                print "Object:", object_names[i]
                print "Stream:", stream_names[i]
                print "Data point:", x
                print ""

                if i == -1 or i == -2:
                    x = illuminance_calc(x)

                # Update database with new data point
                update_point(x, now, object_tags[i], stream_tags[i], base, success=False)

                # Thermometer is last data point;
                # all raw data points have been received.
                # Proceed to determine actuation settings:
                if i == -6:
                    act_sets, time_last_flush, exposure = analysis(exposure, now, time_last_flush)
                    print "Actuation settings:"
                    print act_sets
                    print ""

                    # Send actuation settings to Arduino
                    for key in act_sets:
                        ser.write(act_tags[key])
                        print act_tags[key]
                        time.sleep(1)
                        ser.write(str(act_sets[key]))
                        print act_sets[key]
                        time.sleep(1)
            except:
                print "Error handling sensor data"
        elif i < -100: # valve and pump tags are smaller than -100
            try:
                # Read entire line for actuator state
                s = int(ser.readline())

            except:
                print "Error handling actuator data"

    time.sleep(0.1) # 1 s delay
    return time_last_flush, exp_reset_time, exposure

# Run once at the end
def close():
    try:
        print "Close Serial Port"
        ser.close()
    except:
        print "Close Error"

# Program Structure
def main():
    # Call setup function
    start_time, exp_reset_time, exposure = setup()
    time_last_flush = start_time
    while(True):
        try:
            time_last_flush, exp_reset_time, exposure = loop(time_last_flush, exp_reset_time, exposure)
        except KeyboardInterrupt:
            break # if user enters "Ctrl + C", break while loop
        except:
            # Catch all errors
            print "Unexpected error."
    # Call close function
    close()

# Run the program
main()
