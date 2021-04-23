import serial
import time

# set up the serial line
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

data =[]                       # empty list to store the data
while True:
    b = ser.readline()         # read a byte string
  
    print(ser.readline().decode())
    # add to the end of data list
    time.sleep(0.01)            # wait (sleep) 0.1 seconds

ser.close()