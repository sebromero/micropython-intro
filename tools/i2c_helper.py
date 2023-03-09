from machine import I2C, Pin
import os

# Class to determine the I2C interface based on the board name.
class I2CHelper:
    def get_interface(self, bus=0):
        board_name = os.uname().machine

        if board_name == "Arduino Nano RP2040 Connect with RP2040":
            if bus == 0:
                return I2C(0, scl=Pin(13), sda=Pin(12), freq=100_000)
            elif bus == 1:
                return I2C(1, scl=Pin(7), sda=Pin(6), freq=100_000)
        
        if board_name == "PORTENTA with STM32H747":
            # Alternatively, you can use the I2C bus number instead of the pins. e.g. I2C(1)
            if bus == 0:
                return I2C(scl=Pin('PH7') , sda=Pin('PH8')) #I2C0
            elif bus == 1:
                return I2C(scl=Pin('PB6') , sda=Pin('PB7')) #I2C1
            elif bus == 2:
                # WARNING: This is not a valid I2C bus on the Portenta Breakout V1 due to a hardware bug.
                return I2C(scl=Pin('PH11') , sda=Pin('PH12')) #I2C2
    
        raise ValueError('Unsupported board.')
    