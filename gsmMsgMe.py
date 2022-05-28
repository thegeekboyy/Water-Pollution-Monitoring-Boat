import RPi.GPIO as GPIO
import serial
import time,sys

SERIAL_PORT = "/dev/ttyS0"

ser = serial.Serial(SERIAL_PORT ,baudrate =9600, timeout = 5)
enableSMS = "AT+CMGF=1\r"
ser.write(enableSMS.encode())
print("\nSMS Mode is now enabled")
time.sleep(3)
setNum = 'AT+CMGS="7022501595"\r'
ser.write(setNum.encode())

message = "\rThis SMS was sent through python Script by SIM800"
print("Sending the Pre-stored message")
time.sleep(3)
ser.write(message.encode()+chr(26).encode())
time.sleep(3)
print("Sucess! Your message was delivered :)")