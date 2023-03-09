from machine import Pin, ADC
from time import sleep

def map_range(value, in_min, in_max, out_min, out_max):
    return round(out_min + (((value - in_min) / (in_max - in_min)) * (out_max - out_min)))

# Make sure to follow the GPIO map for the board you are using.
potentiometer = ADC(Pin(26)) # A0 on Nano RP2040 Connect

while True:
    reading = potentiometer.read_u16()     
    #print("ADC: ",reading)
    level = map_range(reading, 176, 65359, 10, 0)
    print(level)
    sleep(0.2)