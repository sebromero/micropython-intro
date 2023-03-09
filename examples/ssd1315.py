from machine import I2C, SoftI2C, Pin
import ssd1306_1315 as ssd

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

i2c_bus = SoftI2C(scl = Pin(13), sda = Pin(12), freq = 100000) # I2C0 on Nano RP2040 Connect
#i2c_bus = I2C(0, scl=Pin(13), sda=Pin(12), freq=100_000) # Throws an exception 🤔
oled = ssd.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c_bus)

oled.text('MicroPython', 20, 20)
oled.text('rocks!', 20, 35)
oled.show()