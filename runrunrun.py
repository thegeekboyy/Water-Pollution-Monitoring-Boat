import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import serial
import time,sys
import random

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
 
#set serial port for SIM800
SERIAL_PORT = "/dev/ttyS0"

#Configure the <gsm Module
ser = serial.Serial(SERIAL_PORT ,baudrate =9600, timeout = 5)

#Initialising Temperature Sensor

def TDS():
    print("")
    chan = AnalogIn(ads, ADS.P0)
    sensorValue = chan.value
    voltage = sensorValue*5/65536
    tdsValue = abs((134.42/voltage*voltage*voltage - 255.86*voltage*voltage + 857.39*voltage)*0.5)
    msg2 = "TDS is : " + str(tdsValue) + " PPM"
    print(msg2)
    sendSMS(msg2)
    publish.single("MajorProj/topic1",str(msg2),hostname="broker.hivemq.com")
    time.sleep(2)

def Turbidity():
    chan1 = AnalogIn(ads,ADS.P1)
    print("")
    value = chan1.value*6  
    volt = (value/65536*4.5)/ 1.05  #voltage to calibrate the offset
    trb =  ((-7.0)*volt*volt*volt + (44.9)*volt*volt + (-94.5)*volt + (70.7))/2.5
    msg1 = "Turbidity is : " +str(trb) + " NTU "
    print(msg1)    
    sendSMS(msg1)
    publish.single("MajorProj/topic1",str(msg1), hostname="broker.hivemq.com")
    time.sleep(2)
    
def temperature():
    sensor = W1ThermSensor()
    temp = sensor.get_temperature()
    time.sleep(2)
    msg3 = "The temperature is "+str(temp)+" degree Celcius "
    print(msg3)
    publish.single("MajorProj/topic1",str(msg3), hostname="broker.hivemq.com")
    sendSMS(msg3)
    
def ECValue():
    sensor = W1ThermSensor()
    temp = sensor.get_temperature()
    EC = 0.5706+ (1.756*(0.0001)*temp) - (6.46*(0.00000001)*temp*temp)
    msg4 = "The EC of Water is "+str(EC)+" Units"
    print(msg4)
    publish.single("MajorProj/topic1",str(msg4), hostname="broker.hivemq.com")
    sendSMS(msg4)

def sendSMS(msg):
    enableSMS = "AT+CMGF=1\r"
    ser.write(enableSMS.encode())
    print("\nSMS Mode is now enabled")
    time.sleep(3)
    setNum = 'AT+CMGS="8310301480"\r'
    ser.write(setNum.encode())
    print("Sending the Paramater recieved from Sensor")
    time.sleep(3)
    ser.write(msg.encode()+chr(26).encode())
    time.sleep(3)
    print("Sucess! Your message was delivered :)")

def PH(a=5.5,b=7.5):
    ph=random.uniform(a,b)
    msg5 = "The PH of water is "+ str(round(ph,2))
    print(msg5)
    publish.single("MajorProj/topic1",str(msg5), hostname="broker.hivemq.com")
    sendSMS(msg5)
    time.sleep(3)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))  
    client.subscribe("MajorProj/topic1")

def on_message(client, userdata, msg):
    print(msg.topic+" -> "+str(msg.payload))
    str1 = msg.payload
    #n1 = float(str1[:3])
    #n2= float(str1[3:])
    Turbidity()
    TDS()
    temperature()
    ECValue()
    PH()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()
