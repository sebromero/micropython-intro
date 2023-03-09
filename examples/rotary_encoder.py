from rotary_irq_rp2 import RotaryIRQ
from time import sleep

# Encoder set to run between 0 and 10, rapping 10 > 0 and 0 > 10
clock_pin = "D10"
data_pin = "D11"
encoder = RotaryIRQ(clock_pin, data_pin, min_val = 0, max_val = 10, range_mode = RotaryIRQ.RANGE_BOUNDED)

value = None

while(True):
    encoder_value = encoder.value()

    if encoder_value != value:
        value = encoder_value
        print("Encoder value: ", encoder_value)
    
    sleep(0.05)