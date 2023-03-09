import time
from machine import Pin

led = Pin(6, Pin.OUT) # Built-in LED on the Nano RP2040 Connect
# led = Pin("D12", Pin.OUT)

while(True):
    led.on()
    time.sleep_ms(500)
    led.off()
    time.sleep_ms(500)
