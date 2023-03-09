from machine import Pin, ADC
from my9221 import MY9221

def map_range(value, in_min, in_max, out_min, out_max):
    return round(out_min + (((value - in_min) / (in_max - in_min)) * (out_max - out_min)))

ledbar = MY9221(Pin(19), Pin(20)) # D7, D8 on Nano RP2040 Connect
ledbar.reverse(True)
adc = ADC(Pin(26)) # GPIO26 = A0 on Nano RP2040 Connect

while True:    
    level = map_range(adc.read_u16(), 176, 65359, 10, 0)
    ledbar.level(level)