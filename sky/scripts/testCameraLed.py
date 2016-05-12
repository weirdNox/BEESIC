#!/usr/bin/env python
import time
import RPi.GPIO as GPIO

# NOTE(nox): This only works when disable_camera_led=1 is set in /boot/config.txt
GPIO.setmode(GPIO.BCM)
CAMLED = 32
GPIO.setup(CAMLED, GPIO.OUT, initial=False)
for _ in range(5):
    GPIO.output(CAMLED,True)
    time.sleep(0.5)
    GPIO.output(CAMLED,False)
    time.sleep(0.5)
