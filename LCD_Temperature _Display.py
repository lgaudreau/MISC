# Using a Raspberry Pi to display the outside temperature and conditions and inside temperature and humidity on a connected LCD.
# Assumes a 2 row LCD connected using I2C and a DHT sensor on pin 17.
# Scheduled to display between 6am - 10am & 5pm - 10pm on weekdays, 6am - 10pm on weekends and turn the display off otherwise.

# todo:
#     implement class for LCD_On variable instead of using "Global LCD_On"
#     find better way of checking for weekends

import time
import datetime
import I2C_LCD_driver
import pyowm
import Adafruit_DHT

Ada_Type = Adafruit_DHT.DHT22
Ada_Pin = 17
mylcd = I2C_LCD_driver.lcd()
LCD_On = True

def GetExternalTemp():
    owm = pyowm.OWM('89152e1d59efc967dab012d7506138d2')
    observation = owm.weather_at_place('Downtown Toronto, CA')
    w = observation.get_weather()
    temp = w.get_temperature('celsius')['temp']
    status = w.get_status()

    return round(temp), str(status)

def GetInternalTemp():
    hum, temp = Adafruit_DHT.read_retry(Ada_Type, Ada_Pin)
    
    return round(hum), round(temp)

def DisplayOnLCD():
        global LCD_On
        out_temp, status = GetExternalTemp()
        humidity, temperature = GetInternalTemp()

        mylcd.lcd_clear()
        mylcd.lcd_display_string("OUT %sC %s" % (str(out_temp)+chr(223),status), 1)
        mylcd.lcd_display_string("IN %sC, %d%% HUM" % (str(temperature) + chr(223), humidity), 2)
        LCD_On = True
        time.sleep(30) 

def main():
    global LCD_On
    date = datetime.date.today()
    today = date.strftime("%a")
    
    while True:
        now = datetime.datetime.now()

        if today == "Sat" or today == "Sun" and now.hour >= 6 and now.hour <= 22:
            DisplayOnLCD()
        
        elif now.hour >= 6 and now.hour <= 10 or now.hour >= 17 and now.hour <= 22:
            DisplayOnLCD() 
                
        else:
            if LCD_On == True:
                mylcd.lcd_clear()
                mylcd.backlight(0)
                LCD_On = False         

main()