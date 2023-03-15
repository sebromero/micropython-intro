from time import sleep
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDM

# create a PWM servo controller
servo_pwm = PWM(Pin("D9"))

# Set the parameters of the servo pulses, more details in the "Documentation" section
frequency = 50
min_us = 544.0
max_us = 2150
max_angle = 180
min_angle = 0

servo = ServoPDM(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=frequency, max_angle=max_angle, min_angle=min_angle, invert=False)
angles = [90, 180, 90, 0]

for angle in angles:
    servo.set_angle(angle)
    sleep(1)

servo.release() # Sets the duty cycle to 0
servo.deinit() # Deinitializes the PWM object