from time import sleep
from lsm6dsox import LSM6DSOX
from machine import I2C

lsm = LSM6DSOX(I2C(0)) # Built-in sensor is on I2C(0) on the Nano RP2040 Connect

while (True):
    print('Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*lsm.read_accel()))
    print('Gyroscope:     x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*lsm.read_gyro()))
    print("")
    sleep(0.1)
