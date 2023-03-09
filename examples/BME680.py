# Library from https://github.com/robert-hh/BME680-Micropython

from bme680 import *
from machine import I2C
import time

bme = BME680_I2C(I2C(1))

while True:
    print()
    print("🌡️ Temperature: %0.1f C" % bme.temperature)
    print("💨 Gas: %d kΩ" % (bme.gas / 1000))
    print("💧 Humidity: %0.1f %%" % bme.humidity)
    print("⛅️ Pressure: %0.1f hPa" % bme.pressure)
    print("⛰️ Altitude = %0.2f meters" % bme.altitude)

    time.sleep(4)