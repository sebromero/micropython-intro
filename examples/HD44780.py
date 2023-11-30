from lcd_i2c import LCD
from machine import I2C, Pin

# PCF8574 on 0x50
I2C_ADDR = 0x27     # DEC 39, HEX 0x27
NUM_ROWS = 2
NUM_COLS = 16

# define custom I2C interface, default is 'I2C(0)'
# check the docs of your device for further details and pin infos
i2c = I2C(0, scl=Pin(15), sda=Pin(13), freq=800000) # Pins on ESP32

for addr in i2c.scan():
    if addr == I2C_ADDR:
        print("Screen Found!")

lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)
lcd.begin()

lcd.backlight()
lcd.blink()
lcd.print("Hello World")