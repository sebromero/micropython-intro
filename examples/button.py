from machine import Pin
import time

button_pin = Pin(25, Pin.IN) # GPIO25 = D2 on Nano RP2040 Connect

while True:
    print(button_pin.value())
    time.sleep(0.1)
