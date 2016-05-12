#!/bin/bash

# NOTE(nox): Volume
amixer cset numid=1 -- 1000

sudo /home/pi/sky/scripts/startGPS.sh &
sudo /home/pi/sky/scripts/testCameraLed.py &
/home/pi/sky/scripts/init.py
