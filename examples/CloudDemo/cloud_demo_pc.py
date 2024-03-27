from time import sleep

for i in range(0, 10):
    print('.')
    sleep(0.1)# This file is part of the Python Arduino IoT Cloud.

# Any copyright is dedicated to the Public Domain.
# https://creativecommons.org/publicdomain/zero/1.0/
import time
import logging

# Import 'arduino_iot_cloud' from the 'lib' folder.
# This is a workaround for the Arduino IDE, which does not support
# importing libraries from the sketch folder.
import sys
sys.path.append("lib")


from arduino_iot_cloud import ArduinoCloudClient
from arduino_iot_cloud import Task

from secrets import DEVICE_ID
from secrets import CLOUD_PASSWORD


def update_sensor_values(client):
    # Update the sensor values.
    # Note: The values are updated in the cloud only if they have changed.

    client["temperature"] = round(23, 1)
    client["humidity"] = 45
    client["pressure"] = round(2500, 1)
    client["gas"] = 124440 / 1000
    client["altitude"] = 420

# Switch callback, toggles the LED.
def on_led_changed(client, value):
    print("LED changed")

if __name__ == "__main__":
    # Configure the logger.
    # All message equal or higher to the logger level are printed.
    # To see more debugging messages, set level=logging.DEBUG.
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(message)s",
        level=logging.INFO,
    )

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