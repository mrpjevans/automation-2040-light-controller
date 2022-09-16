from automation import *
from machine import Pin, I2C
import time

import veml7700

board = Automation2040W()

# Change these values to meet your needs
darkness_threshold = 50
delay_after_darkness = 5 # Seconds

# Setup sensors
i2c = board.i2c
lux_sensor = veml7700.VEML7700(address=0x10, i2c=i2c, it=100, gain=1/8)

led_strip_on = False
board.conn_led(False)
darkness_detected = False

print("Running")
while True:
    # Check for motion only if the lights are off
    if not led_strip_on:
        motion_level = board.read_adc(0)
        if motion_level > 1:
            print("Motion detected, lights on")
            board.conn_led(True)
            board.output(0, True)
            led_strip_on = True
    else:
        if lux_sensor.read_lux() <= darkness_threshold:
            if not darkness_detected:
                darkness_detected = True
                print("It's dark!")
                time.sleep(delay_after_darkness)
            else:
                print("Still dark, lights off")
                darkness_detected = False
                board.conn_led(False)
                board.output(0, False)
                led_strip_on = False
                time.sleep(delay_after_darkness)
                print("Monitoring again")
            
    time.sleep(0.5)

