# automation-2040-light-controller
The MagPi - Tutorial for controlling lights using Automation 2040 W

Please see Issue 123 for full instructions

## In This Repo

### main_sourcing.py

Power the LED light strip directly from Automation 2040 W

(Check the power requirements carefully before going this route!)

### main_relay.py

Control the lights using Relay 3 to swicth the power supply (Max 40V 2A)

### main_relay_pushover.py

Send alerts to a Pushover account when the state changes (see pushover.net)

### main_relay_mqtt.py

Send updates to a MQTT broker when the state changes

## Dependancies

All scripts require `velm7700.py` (included in this repo) to read the light sensor

`main_relay_mqtt.py` requires `umqtt_simple.py` to send MQTT updates

In both cases place upload the files using Thonny to the root of the Raspberry Pi Pico W.

## Additional Libraries

### veml7700.py
Copyright (c) 2019 Joseph Hopfmüller

This module is a fork of Christophe Rousseaus module. 

https://github.com/palouf34/veml7700.git

### umqtt_simple.py
https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.simple/umqtt/simple.py
