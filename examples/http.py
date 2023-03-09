# Simple HTTP client example.

import network, socket
from secrets import WIFI_SSID
from secrets import WIFI_PASSWORD

def connect_to_wifi(ssid, key):
    interface = network.WLAN(network.STA_IF)
    if not interface.isconnected():
        print('Connecting to network...')
        interface.active(True)
        interface.connect(ssid, key)
        while not interface.isconnected():
            print("Waiting for connection...")
            pass
    return interface.ifconfig()    

def fetch_url(url, port=80):
    _, _, host, path = url.split('/', 3)

    # Get addr info via DNS
    addr = socket.getaddrinfo(host, port)[0][4]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    client.settimeout(3.0)
    client.send(f"GET /{path} HTTP/1.1\r\nHost: {host}\r\n\r\n")
    data = client.recv(1024)
    client.close()
    return data


if not WIFI_SSID or not WIFI_PASSWORD:
    raise (Exception("Network is not configured. Set SSID and passwords in secrets.py"))

print("Trying to connect. This may take a while...")
print('WiFi Connected:', connect_to_wifi(WIFI_SSID, WIFI_PASSWORD))
data = fetch_url("http://www.google.com/")
print(data)