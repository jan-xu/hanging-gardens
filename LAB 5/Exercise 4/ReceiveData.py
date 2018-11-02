"""
    Simple program structure
    
"""
import serial
# Change the port name to match the port
# to which your Arduino is connected.
serial_port_name = '/dev/cu.usbserial-DN01J2G2' # for Mac 
ser = serial.Serial(serial_port_name, 9600, timeout=1)

import time

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
        if ser.readline() == 1 | ser.readline() == 2:
            i = ser.readline()
            break
        try:
            # Read entire line 
            # (until '\n')
            x = ser.readline()
            print "Received:", x 
            print "Type:", type(x)
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
