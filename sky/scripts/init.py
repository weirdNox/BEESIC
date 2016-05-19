#!/usr/bin/python
# Init script for Sky Pi
import logging
import os
import time
import threading
import sys
import subprocess
import picamera
import Adafruit_BMP.BMP085 as BMP085
from gps import *

fileId = ""
speakLock = threading.Lock()
speakProcess = None
gpsd = None

# NOTE(nox): Speaking
def speakWorker(msg):
    speakLock.acquire()
    espeakProcess = subprocess.Popen(["espeak", "-s100", msg, "--stdout"], stdout=subprocess.PIPE)
    aplayProcess = subprocess.Popen(["aplay"], stdin=espeakProcess.stdout)
    aplayProcess.communicate()
    speakLock.release()

def speak(msg):
    t = threading.Thread(target=speakWorker, args=(msg,))
    t.start()

# NOTE(nox): Camera
def cameraWorker():
    logging.info("CAMERA: Starting up")
    camera = picamera.PiCamera()
    fileId = 0

    while True:
        try:
            for i in xrange(fileId, sys.maxint):
                if not(os.path.isfile("data/videos/{}.h264".format(i))):
                    fileId = i
                    break

            videoFile = "data/videos/{}.h264".format(fileId)
            logging.info("CAMERA: Writing video " + videoFile)
            camera.start_recording(videoFile)
            time.sleep(300)
            camera.stop_recording()
            logging.info("CAMERA: Wrote video " + videoFile)
        except:
            logging.error("CAMERA: Something went wrong")
            time.sleep(60)

# NOTE(nox): Sensors
def sensorsWorker():
    logging.info("SENSORS: Starting up")

    firstTime = False
    if not(os.path.isfile("data/sensors.csv")):
        firstTime = True

    sensorsFile = open("data/sensors.csv", "a")
    if firstTime:
        sensorsFile.write("sep=,\n")

    sensorsFile.write("TIME,TEMPERATURE,PRESSURE\n")

    bmp180 = None
    bmp180FailedLast = False
    while True:
        temp = -5000
        pressure = -5000
        try:
            if bmp180 == None:
                bmp180 = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

            temp = bmp180.read_temperature()
            pressure = bmp180.read_pressure()

            if bmp180FailedLast:
                logging.info("SENSORS: BMP180 recovered")
                speak("BMP180 recovered")
                bmp180FailedLast = False
        except:
            if not(bmp180FailedLast):
                bmp180FailedLast = True
                logging.error("SENSORS: BMP180 failed")
                speak("BMP180 failed")

        timeStr = time.strftime("%H:%M:%S")
        sensorsFile.write("{},{},{}\n".format(timeStr, temp, pressure))
        sensorsFile.flush()
        time.sleep(2)

# NOTE(nox): GPS
def gpsPoll():
    global gpsd
    while gpsd != None:
        report = gpsd.next()

def gpsWorker():
    logging.info("GPS: Starting up")

    global gpsd
    gpsd = gps(mode=WATCH_ENABLE)

    gpsPollThread = threading.Thread(target=gpsPoll)
    gpsPollThread.start()

    firstTime = False
    if not(os.path.isfile("data/gps.csv")):
        firstTime = True

    gpsFile = open("data/gps.csv", "a")
    if firstTime:
        gpsFile.write("sep=,\n")

    gpsFile.write("TIME,LATITUDE (deg+-m),LONGITUDE (deg+-m),ALTITUDE (m+-m),TRACK (deg from true north+-deg),SPEED (m/s+-m/s),CLIMB (m/s+-m/s),MODE,SAT\n")

    cooldown = 20
    cgpsCooldown = 60
    while True:
        if cooldown >= 20:
            cooldown = 0
            speak("Latitude: {}, Longitude: {}, Altitude: {}".format(gpsd.fix.latitude,
                                                                     gpsd.fix.longitude,
                                                                     gpsd.fix.altitude))
            if gpsd.utc is not None:
	        gpstime = gpsd.utc[0:4] + gpsd.utc[5:7] + gpsd.utc[8:10] + ' ' + gpsd.utc[11:19]
	        os.system('sudo date --set="%s"' % gpstime)

        gpsFile.write("{}+-{},{}+-{},{}+-{},{}+-{},{}+-{},{}+-{},{}+-{},{},{}\n".format(
            gpsd.utc, gpsd.fix.ept, gpsd.fix.latitude, gpsd.fix.epy, gpsd.fix.longitude,
            gpsd.fix.epx, gpsd.fix.altitude, gpsd.fix.epv, gpsd.fix.track, gpsd.fix.epd,
            gpsd.fix.speed, gpsd.fix.eps, gpsd.fix.climb, gpsd.fix.epc, gpsd.fix.mode,
            len(gpsd.satellites)))
        gpsFile.flush()

        if cgpsCooldown >= 60:
            cgpsCooldown = 0
            subprocess.Popen(["scripts/testGPS.sh"])

        cooldown += 1
        cgpsCooldown += 1
        time.sleep(1)


if __name__ == "__main__":
    if not os.path.isdir("data/"):
        os.makedirs("data/")
    if not os.path.isdir("data/videos/"):
        os.makedirs("data/videos/")

    root = logging.getLogger()
    fileHandler = logging.FileHandler("data/log.txt")
    fileHandler.setFormatter(logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(message)s"))
    root.addHandler(fileHandler)
    root.setLevel(logging.INFO)

    logging.info("=============== RESTART ===============")
    logging.info("Starting up...")
    speak("Starting up...")

    # NOTE(nox): Startup worker threads
    cameraThread = threading.Thread(target=cameraWorker)
    cameraThread.start()
    sensorsThread = threading.Thread(target=sensorsWorker)
    sensorsThread.start()
    gpsThread = threading.Thread(target=gpsWorker)
    gpsThread.start()

    time.sleep(20)
    logging.info("Done starting systems.")
    speak("Up and running!")

    while True:
        time.sleep(10)
