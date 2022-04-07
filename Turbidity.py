import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

while True:
	
    acc = 0
	for i in range(0,800):
		chan = AnalogIn(ads, ADS.P0)
		value = chan.value*6
		volt1 = (value/65536*4.5)/ 1.05 
		acc = acc + volt1

	volt = acc/800
    trb =  ((-7.0)*volt*volt*volt + (44.9)*volt*volt + (-94.5)*volt + (70.7))/2.5
    print("Volatge : ",volt," V")
    print("Value   :",trb," NTU")


