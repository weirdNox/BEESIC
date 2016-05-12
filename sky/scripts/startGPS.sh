#!/bin/bash
killall -9 gpsd ntpd
sleep 5
gpsd -n /dev/ttyACM0 &
