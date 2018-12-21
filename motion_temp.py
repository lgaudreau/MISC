#!/usr/bin/env python

# Using a Raspberry Pi to detect motion and display the time & date.
# Assumes a 2 row LCD connected using I2C and a PIR motion detector with the data connected on board pin 7 (gpio4).
# Will show the current date and time if it detects motion, checking every 20min but the display updats seconds/minutes in real time.  
# If it does not detect motion after 20min, will turn the display off and check for further motion.  

# OpenWeatherMap API
# 89152e1d59efc967dab012d7506138d2


import RPi.GPIO as GPIO
import time
import I2C_LCD_driver
import pyowm
from sense_emu import SenseHat
sense = SenseHat()

GPIO.setmode(GPIO.BOARD)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)

mylcd = I2C_LCD_driver.lcd()

print ("PIR Module Running (CTRL+C to exit)")
time.sleep(2)
print ("Ready")

logpath = "/home/pi/Documents/pylog.txt"

with open(logpath,"w") as log:
    log.write("State, Time, Temperature\n" )

def WriteLog(state, time, temp):
    with open(logpath,"a+") as log:
        log.write("%s, %s, %s\n" % (state, time, temp))

def GetTemp():
    owm = pyowm.OWM('89152e1d59efc967dab012d7506138d2')
    observation = owm.weather_at_place('Downtown Toronto, CA')
    w = observation.get_weather()
    temp = w.get_temperature('celsius')['temp']

    return int(round(temp))
    
def main():
    while(1):
        if GPIO.input(PIR_PIN) == 0:
           mylcd.backlight(0)
           with open(logpath, 'r') as f:
                lines = f.read().splitlines()
                last_line = lines[-1]
                if ("ON" in last_line) or ("State" in last_line):
                    WriteLog("OFF",time.strftime('%I:%M:%S %p'),GetTemp())
        else:
            start_time = time.time()
            check_time = start_time + 1200
            curtemp = GetTemp()
            with open(logpath, 'r') as f:
                lines = f.read().splitlines()
                last_line = lines[-1]
                if ("OFF" in last_line) or ("State" in last_line):
                    WriteLog("ON",time.strftime('%I:%M:%S %p'),curtemp)
            while time.time() < check_time:
                humidity = str(int(round(sense.humidity)))
                temperature = str(int(round(sense.temperature)))
                mylcd.lcd_display_string("Outside %sC" % (str(curtemp)+chr(223)), 1)
                mylcd.lcd_display_string("%sC, %s HUM" % (temperature + chr(223), humidity), 2)
                
main()