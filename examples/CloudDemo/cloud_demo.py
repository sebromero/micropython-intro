from time import sleep

for i in range(0, 10):
    print('.')
    sleep(0.1)# This file is part of the Python Arduino IoT Cloud.

# Any copyright is dedicated to the Public Domain.
# https://creativecommons.org/publicdomain/zero/1.0/
import time
import network
import logging
from random import random
from machine import I2C, Pin
from arduino_iot_cloud import ArduinoCloudClient
from arduino_iot_cloud import Task

from secrets import WIFI_SSID
from secrets import WIFI_PASSWORD
from secrets import DEVICE_ID
from secrets import CLOUD_PASSWORD

bme = None
try:
    from bme680 import *
    bme = BME680_I2C(I2C(1))
except ImportError:
    print("❌ BME680 library not found.")
except OSError as e:
    print("❌ Couldn't connect to the BME680 module." + str(e))
    bme = None    
finally:
    if bme is None:
        class DummyBME680:
            @property
            def temperature(self):
                # Return random number between 20 and 30.
                return 20 + (30 - 20) * random()
            
            @property
            def humidity(self):                
                # Return random number between 20 and 100.
                return 20 + (100 - 20) * random()
            
            @property
            def pressure(self):
                # Return random number between 200 and 1200.
                return 200 + (1200 - 200) * random()
            
            @property
            def gas(self):
                # Return random number between 1000 and 100000.
                return int(1000 + (100000 - 1000) * random())
            
            @property
            def altitude(self):
                # Return random number between 0 and 1500.
                return 0 + (1500 - 0) * random()

        print("🤖 BME680 module not found. Using dummy values.")
        bme = DummyBME680()

led = Pin("LED_BUILTIN", Pin.OUT)

def wifi_connect():
    if not WIFI_SSID or not WIFI_PASSWORD:
        raise (Exception("Network is not configured. Set SSID and passwords in secrets.py"))
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        logging.info("Trying to connect. Note this may take a while...")
        time.sleep_ms(500)
    logging.info(f"WiFi Connected {wlan.ifconfig()}")

def update_sensor_values(client):
    # Update the sensor values.
    temperature = round(bme.temperature, 1)
    humidity = bme.humidity
    pressure = round(bme.pressure, 1)
    gas = bme.gas / 1000
    altitude = bme.altitude

    print("🌡️ Temperature: %0.1f C" % temperature)
    print("💨 Gas: %d kOhm" % gas)
    print("💧 Humidity: %0.1f %%" % humidity)
    print("⛅️ Pressure: %0.1f hPa" % pressure)
    print("⛰️ Altitude = %0.2f meters" % altitude)

    # Update the cloud values.
    # Note: The values are updated in the cloud only if they have changed.
    client["temperature"] = temperature
    client["humidity"] = humidity
    client["pressure"] = pressure
    client["gas"] = gas
    client["altitude"] = altitude

# Switch callback, toggles the LED.
def on_led_changed(client, value):
    print("LED changed")
    led.value(value)

if __name__ == "__main__":
    # Configure the logger.
    # All message equal or higher to the logger level are printed.
    # To see more debugging messages, set level=logging.DEBUG.
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(message)s",
        level=logging.INFO,
    )

    # NOTE: Add networking code here or in boot.py
    wifi_connect()

    # 1. Create a client object, which is used to connect to the IoT cloud and link local
    # objects to cloud objects. Note a username and password can be used for basic authentication
    # on both CPython and MicroPython. For more advanced authentication methods, please see the examples.
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=CLOUD_PASSWORD)
    
    # 2. Register cloud objects.
    # Note: The following objects must be created first in the dashboard and linked to the device.
    # When the switch is toggled from the dashboard, the on_switch_changed function is called with
    # the client object and new value args.
    
    # The LED object is updated in the on_write callback.
    client.register("led", value=None, on_write=on_led_changed)
    client.register("temperature", value=None)
    client.register("humidity", value=None)
    client.register("pressure", value=None)
    client.register("gas", value=None)
    client.register("altitude", value=None)    
    client.register(Task("sensor_update", on_run=update_sensor_values, interval=5.0))

    # 3. Start the Arduino cloud client.
    client.start()