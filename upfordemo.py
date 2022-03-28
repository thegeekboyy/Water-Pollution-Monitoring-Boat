import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

def TDS():
    print("")
    chan = AnalogIn(ads, ADS.P0)
    # print("The Value from TDS Sensor :",chan.value)
    # print("The Equivalent Voltage is :",chan.voltage)
    sensorValue = chan.value
    voltage = sensorValue*5/65536
    tdsValue = (134.42/voltage*voltage*voltage - 255.86*voltage*voltage + 857.39*voltage)*0.5
    mzg = "TDS is : " + str(tdsValue) + " PPM"
    print("The TDS of the water Sample is : ",tdsValue," PPM")
    publish.single("MajorProj/topic1",str(mzg),hostname="broker.hivemq.com")
    time.sleep(2)

def Turbidity():
    chan1 = AnalogIn(ads,ADS.P1)
    print("")
    value = chan1.value*6
    volt = (value/65536*4.5)/ 1.05  #voltage to calibrate the offset
    trb =  ((-7.0)*volt*volt*volt + (44.9)*volt*volt + (-94.5)*volt + (70.7))/2.5
    print("Turbidity of water sample is : ",trb," NTU ") 
#     print("The Value from Turbidity Sensor :",chan1.value)
   #s print("The Equivalent Voltage is :",chan1.voltage)
    mzg1 = "Turbidity is : " +str(trb) + " NTU "
    publish.single("MajorProj/topic1",str(mzg1), hostname="broker.hivemq.com")
    time.sleep(2)




def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))  
    client.subscribe("MajorProj/topic1")

def on_message(client, userdata, msg):
    print(msg.topic+""+str(msg.payload))
    Turbidity()
    TDS()
    
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()

