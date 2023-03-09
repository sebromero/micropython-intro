from machine import Pin
from my9221 import MY9221
from time import sleep

# Need to use the GPIO numbers, not the labeled pin names
# SEE: https://github.com/micropython/micropython/blob/master/ports/rp2/boards/ARDUINO_NANO_RP2040_CONNECT/pins.csv
ledbar = MY9221(Pin(19), Pin(20)) # D7, D8 on Nano RP2040 Connect
ledbar.reverse(True)

# Turn LEDS on one at a time, full brightness
for i in range(0, 11):
    ledbar.level(i)
    sleep(0.2)

# Alternate LEDs
for i in range(0, 5):
    ledbar.bits(0b0101010101)
    sleep(0.2)
    ledbar.bits(0b1010101010)
    sleep(0.2)
    
# Fade out LEDs
for i in range(255, -1, -5):
    ledbar.level(10, brightness=i)
    sleep(0.02)