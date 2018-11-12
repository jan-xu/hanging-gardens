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

# Change the port name to match the port to which Arduino is connected
serial_port_name = '/dev/cu.usbserial-DN01J2G2' # for Mac
ser = serial.Serial(serial_port_name, 9600, timeout=1)

# Set up network ID
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

stream_tags = {
    -1: 'left_light',
    -2: 'right_light',
    -3: 'center_light',
    -4: 'lower_water_level',
    -5: 'upper_water_level',
    -6: 'temperature'
}

# Define setup function that runs once at the start
def setup():
    try:
        print "Setup"
    except:
        print "Setup Error"

# Define setup function that runs continuously forever
def loop():
    # Check if something is in serial buffer
    if ser.inWaiting() > 0:
        i = int(ser.readline())
        if i < 0:
            print datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            print "Object:", object_tags[i]
            print "Stream:", stream_tags[i]

            try:
                # Read entire line (until '\n')
                x = int(ser.readline())
                print "Data point:", x
                print ""

                #if int(i) == 1:
                query = {
                    'object-name': object_names[i]
                }
                endpoint = '/networks/'+network_id+'/objects/'+object_tags[i]
                response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120)
                resp = json.loads(response.text)
                if resp['object-code'] == 201:
                    print 'Create object: ok'
                else:
                    print 'Create object: error'
                    print response.text

                query = {
                    'stream-name': stream_tags[i],
                    'points-type': 'i' # 'i', 'f', or 's'
                }
                endpoint = '/networks/'+network_id+'/objects/'+object_tags[i]+'/streams/'+stream_tags[i]
                response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120)
                resp = json.loads(response.text)
                if resp['stream-code'] == 201:
                    print 'Create stream: ok'
                else:
                    print 'Create stream: error'
                    print response.text

                endpoint = '/networks/'+network_id+'/objects/'+object_tags[i]+'/streams/'+stream_tags[i]+'/points/'
                query = {
                    'points-value': x,
                    'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                }
                response = requests.request('POST', base + endpoint, params=query, headers=header, timeout=120)
                resp = json.loads(response.text)
                if resp['points-code'] == 200:
                    print 'Update data points: ok'
                else:
                    print 'Update data points: error'
                    print response.text

            except:
                print "Error"

    time.sleep(0.1) # 100 ms delay

# Run continuously forever with a delay between calls
def delayed_loop():
    print "Delayed Loop"

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
    setup()
    # Set start time
    nextLoop = time.time()
    while(True):
        # Try loop() and delayed_loop()
        try:
            loop()
            if time.time() > nextLoop:
                # If next loop time has passed
                nextLoop = time.time() + delay
                delayed_loop()
        except KeyboardInterrupt:
            break # if user enters "Ctrl + C", break while loop
        except:
            # Catch all errors
            print "Unexpected error."
    # Call close function
    close()

# Run the program
main()
