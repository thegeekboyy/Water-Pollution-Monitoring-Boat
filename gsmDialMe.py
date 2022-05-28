import RPi.GPIO as GPIO
import serial
import time,sys

SERIAL_PORT="/dev/ttyS0"
ser=serial.Serial(SERIAL_PORT,baudrate = 9600,timeout=5)

toCall ="ATD7022501595;\r"
ser.write(toCall.encode())
print("Calling.....")
time.sleep(30)
for each in range(1,11):
    print(each, end = " ")
toHangUp = "ATH\r"
ser.write(toHangUp.encode())
print("\nHanging Up.....")