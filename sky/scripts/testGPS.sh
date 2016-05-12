#!/bin/bash
/usr/bin/gpsmon &
sleep 5
sudo killall gpsmon
