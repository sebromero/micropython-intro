from machine import Pin
from time import sleep_ms
import math

pwm = machine.PWM(Pin("D12"))
pwm.freq(1000)
max_duty = 2**16
steps = 60

while True:
    for i in range(steps):
        duty = int(math.sin(i / (steps / 2) * math.pi) * (max_duty / 2) + (max_duty / 2)) # Range 0 - 65535
        pwm.duty_u16(duty)
        sleep_ms(40)