
import network
import urequests
import json
from automation import *
from machine import Pin, I2C
import time

import veml7700
from umqtt_simple import MQTTClient

board = Automation2040W()

# Change these to match your settings
ssid = "SecretUndergroundLair"
password = "abacab0001!"
mqtt_broker = "192.168.1.10"
mqtt_topic = b"study/leds"
mqtt_client_id = b"Automation 2040 W"

# Change these values to meet your needs
darkness_threshold = 50
delay_after_darkness = 5 # Seconds

# Connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
print("Wifi status: " + str(wlan.isconnected()))

# Connect to MQTT
client = MQTTClient(mqtt_client_id, mqtt_broker, keepalive=3600)
client.connect()
print("Connected to MQTT Broker")

# Setup sensors
i2c = board.i2c
lux_sensor = veml7700.VEML7700(address=0x10, i2c=i2c, it=100, gain=1/8)

led_strip_on = False
board.conn_led(False)
darkness_detected = False

def mqtt(message):
    print(message)
    client.publish(mqtt_topic, message)

print("Running")
while True:
    # Check for motion only if the lights are off
    if not led_strip_on:
        motion_level = board.read_adc(0)
        if motion_level > 1:
            mqtt("Motion detected, lights on")
            board.conn_led(True)
            board.relay(2, True)
            led_strip_on = True
    else:
        if lux_sensor.read_lux() <= darkness_threshold:
            if not darkness_detected:
                darkness_detected = True
                mqtt("It's dark!")
                time.sleep(delay_after_darkness)
            else:
                mqtt("Still dark, lights off")
                darkness_detected = False
                board.conn_led(False)
                board.relay(2, False)
                led_strip_on = False
                time.sleep(delay_after_darkness)
                mqtt("Monitoring again")
            
    time.sleep(0.5)

