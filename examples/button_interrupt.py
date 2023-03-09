from machine import Pin

def callback(pin):
  if pin.value() == 1:
    print("Button pressed")
  else:
    print("Button released")
  
button = Pin(25, Pin.IN) # GPIO25 = D2 on Nano RP2040 Connect
button.irq(handler=callback) # trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING) is default