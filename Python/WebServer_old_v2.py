'''

University of California, Berkeley
CE 186 Design of Cyber-Physical Systems (Fall Term 2018)
Hanging Gardens: WebServer.py
Group 6

DESCRIPTION

'''

# Import required modules
import serial
import time
import requests
import json
import datetime
import pytz
from DataAnalysis import analysis

# Change the port name to match the port to which Arduino is connected
serial_port_name = '/dev/cu.usbmodem144401' # for Mac
ser = serial.Serial(serial_port_name, 9600, timeout=1)

# Set up network details
base = 'http://127.0.0.1:5000'
network_id = 'local'
header = {}

# Define parameters
delay = 10 # [s] -- delay

object_names = {
    -1: 'Light Sensor',
    -2: 'Light Sensor',
    -3: 'Light Sensor',
    -4: 'Water Lever Meter',
    -5: 'Water Lever Meter',
    -6: 'Thermometer'
}

object_tags = {
    -1: 'light_sensor',
    -2: 'light_sensor',
    -3: 'light_sensor',
    -4: 'water_level_meter',
    -5: 'water_level_meter',
    -6: 'thermometer'
}

stream_names = {
    -1: 'Left Light Sensor',
    -2: 'Right Light Sensor',
    -3: 'Center Light Sensor',
    -4: 'Lower Water Level',
    -5: 'Upper Water Level',
    -6: 'Temperature'
}

stream_tags = {
    -1: 'left_light',
    -2: 'right_light',
    -3: 'center_light',
    -4: 'lower_water_level',
    -5: 'upper_water_level',
    -6: 'temperature'
}

'''
actuator_tags = {
    'LED': 2,
    PP_tag = 3;
    int Vlwr_tag = 4;
    int Vupr_tag = 5;
    int Srv_tag = 6;
}
'''


# Define setup function that runs once at the start
def setup():
    try:
        print "Setup"
        print ""
        start_time = datetime.datetime.utcnow()
        return start_time
    except:
        print "Setup Error"
        print ""

# Define setup function that runs continuously forever
def loop(time_last_flush):
    t = 0
    # Check if something is in serial buffer
    if ser.inWaiting() > 0:
        i = int(ser.readline())
        if i < 0:
            try:
                now = datetime.datetime.utcnow()
                print now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                print "Object:", object_tags[i]
                print "Stream:", stream_tags[i]

                # Read entire line (until '\n')
                x = int(ser.readline())
                print "Data point:", x

                query = {
                    'object-name': object_names[i]
                }
                endpoint = '/networks/'+network_id+'/objects/'+object_tags[i]
                response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120)
                resp = json.loads(response.text)
                if resp['object-code'] == 201:
                    print 'Create object: ok'
                #else:
                    #print 'Create object: error'
                    #print response.text

                if i == -6:
                    query = {
                        'stream-name': stream_names[i],
                        'points-type': 'f' # 'i', 'f', or 's'
                    }
                else:
                    query = {
                        'stream-name': stream_names[i],
                        'points-type': 'i' # 'i', 'f', or 's'
                    }
                endpoint = '/networks/'+network_id+'/objects/'+object_tags[i]+'/streams/'+stream_tags[i]
                response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120)
                resp = json.loads(response.text)
                if resp['stream-code'] == 201:
                    print 'Create stream: ok'
                #else:
                    #print 'Create stream: error'
                    #print response.text

                endpoint = '/networks/'+network_id+'/objects/'+object_tags[i]+'/streams/'+stream_tags[i]+'/points'
                query = {
                    'points-value': x,
                    'points-at': now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                }
                response = requests.request('POST', base + endpoint, params=query, headers=header, timeout=120)
                resp = json.loads(response.text)
                if resp['points-code'] == 200:
                    print 'Update raw data points: ok'
                else:
                    print 'Update raw data points: error'
                    print response.text

                if i == -3:
                    t = 2
                    light = x
                else:
                    t = 1
                ## UPLOAD INFO ABOUT ENERGY USAGE FOR LED
            except:
                print "Error"
    if t != 0:
        act_sets, time_last_flush = analysis(time_last_flush, t)
        print act_sets
        print ""
    time.sleep(1) # 1 s delay
    return time_last_flush

# Run continuously forever with a delay between calls
def delayed_loop():
    print "Delayed Loop"
    print ""

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
    start_time = setup()
    time_last_flush = start_time
    while(True):
        try:
            time_last_flush = loop(time_last_flush)
            # RECORD WHEN LED IS ON
            # READ TAGS FOR PUMP AND VALVES

            #if time.time() > nextLoop:
                # If next loop time has passed
                #nextLoop = time.time() + delay
                #delayed_loop()
        except KeyboardInterrupt:
            break # if user enters "Ctrl + C", break while loop
        except:
            # Catch all errors
            print "Unexpected error."
    # Call close function
    close()

# Run the program
main()
