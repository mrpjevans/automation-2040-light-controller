import network
import urequests
import json
from automation import *
from machine import Pin, I2C
import time

import veml7700

board = Automation2040W()

# Change these to match your settings
ssid = "<Your wifi network name>"
password = "<Your wifi network password>"
pushover_user_token = "<Pushover user token>"
pushover_api_token = "<Pushover API/app token>"

# Change these values to meet your needs
darkness_threshold = 50
delay_after_darkness = 5 # Seconds

# Connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
print("Wifi status: " + str(wlan.isconnected()))

# Setup sensors
i2c = board.i2c
lux_sensor = veml7700.VEML7700(address=0x10, i2c=i2c, it=100, gain=1/8)

led_strip_on = False
board.conn_led(False)
darkness_detected = False

def pushover(message):
    print(message)
    payload = "token={}&user={}&title=Lights&message={}".format(pushover_api_token, pushover_user_token, message)
    urequests.post("https://api.pushover.net/1/messages.json", data=payload)

print("Running")
while True:
    # Check for motion only if the lights are off
    if not led_strip_on:
        motion_level = board.read_adc(0)
        if motion_level > 1:
            pushover("Motion detected, lights on")
            board.conn_led(True)
            board.relay(2, True)
            led_strip_on = True
    else:
        if lux_sensor.read_lux() <= darkness_threshold:
            if not darkness_detected:
                darkness_detected = True
                pushover("It's dark!")
                time.sleep(delay_after_darkness)
            else:
                pushover("Still dark, lights off")
                darkness_detected = False
                board.conn_led(False)
                board.relay(2, False)
                led_strip_on = False
                time.sleep(delay_after_darkness)
                pushover("Monitoring again")
            
    time.sleep(0.5)

