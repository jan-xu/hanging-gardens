"""
    Simple program structure
    
"""
import serial
# Change the port name to match the port
# to which your Arduino is connected.
serial_port_name = '/dev/cu.usbserial-DN01J2G2' # for Mac 
ser = serial.Serial(serial_port_name, 9600, timeout=1)

import time

#############
import requests
import json
import random
#import time
import datetime

base = 'http://127.0.0.1:5000'
network_id = 'local'
header = {}
#############

delay = 1*10 # Delay in seconds

# Run once at the start
def setup():
    try:
        print "Setup"
    except:
        print "Setup Error"

# Run continuously forever
def loop():
    # Check if something is in serial buffer \
    if ser.inWaiting() > 0:
        i = ser.readline()
        if int(i) == 1 or int(i) == 2:
            print "Received tag:", i
            print "Type tag:", type(i)
        try:
            # Read entire line 
            # (until '\n')
            x = ser.readline()
            print "Received data:", x 
            print "Type data:", type(x)
            
            ###################################################################################################
            if int(i) == 1:
                query = {
                    'object-name': 'Test Object'
                }
                endpoint = '/networks/'+network_id+'/objects/test-object'
                response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
                resp = json.loads( response.text )
                if resp['object-code'] == 201:
                    print('Create object test-object: ok')
                else:
                    print('Create object test-object: error')
                    print( response.text )
       
                query = {
                    'stream-name': 'Test Stream',
                    'points-type': 'i' # 'i', 'f', or 's'
                }
                endpoint = '/networks/'+network_id+'/objects/test-object/streams/test-stream'
                response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
                resp = json.loads( response.text )
                if resp['stream-code'] == 201:
                    print('Create stream test-stream: ok')
                else:
                    print('Create stream test-stream: error')
                    print( response.text )
    
    
                print("Start sending random points (Ctrl+C to stop)")
                endpoint = '/networks/local/objects/test-object/streams/test-stream/points'
    
                    
                query = {
                    'points-value': int(x),
                    'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                }
                response = requests.request('POST', base + endpoint, params=query, headers=header, timeout=120 )
                resp = json.loads( response.text )
                if resp['points-code'] == 200:
                    print( 'Update test-stream points: ok')
                else:
                    print( 'Update test-stream points: error')
                    print( response.text )
            
            ###################################################################################################

            
        except:
            print "Error"
            
    # 100 ms delay
    time.sleep(0.1)
    return


# Run continuously forever
# with a delay between calls
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
                # If next loop time has passed...
                nextLoop = time.time() + delay
                delayed_loop()
        except KeyboardInterrupt:
            # If user enters "Ctrl + C", break while loop
            break
        except:
            # Catch all errors
            print "Unexpected error."
    # Call close function
    close()

# Run the program
main()
