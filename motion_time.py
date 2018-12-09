#!/usr/bin/env python

# Assumes a 2 row LCD connected on 27 and a PIR motion detector with the data connected on board pin 7 (gpio4).
# Will show the current date and time if it detects motion, checking every 20min but the display updats seconds/minutes in real time.  
# If it does not detect motion after 20min, will turn the display off and check for further motion.  

import RPi.GPIO as GPIO
import time
import I2C_LCD_driver

GPIO.setmode(GPIO.BOARD)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)

mylcd = I2C_LCD_driver.lcd()

print ("PIR Module Test (CTRL+C to exit)")
time.sleep(2)
print ("Ready")

next_time = 0
count = 0

def main():
    while(1):
        if GPIO.input(PIR_PIN) == 0:
           mylcd.backlight(0)
        else:
            # print ("Motion Detected") # helpful while testing
            start_time = time.clock()
            check_time = start_time + 1200
            while time.clock() < check_time:
                mylcd.lcd_display_string(time.strftime('%I:%M:%S %p'), 1)
                mylcd.lcd_display_string(time.strftime('%a %b %d, 20%y'), 2)
             
main()
