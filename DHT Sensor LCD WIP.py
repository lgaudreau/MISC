# pip install pyowm

import pyowm
import time

logpath = "c:\users\lgaudreau\desktop\pylog.txt"

with open(logpath,"w") as log:
    log.write("OFF, %s, Begin Log\n" % time.strftime('%I:%M %p'))

def WriteLog(state, time, temp):
    with open(logpath,"a+") as log:
        log.write("%s, %s, %s\n" % (state, time, temp))

def GetTemp():
    owm = pyowm.OWM('89152e1d59efc967dab012d7506138d2')  # You MUST provide a valid API key
    observation = owm.weather_at_place('Toronto,CA')
    w = observation.get_weather()
    temp = w.get_temperature('celsius')['temp']  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

    return str(int(round(temp)))


curtemp = "Current temperature in Toronto is %s" % GetTemp() + chr(223)

print (curtemp)

WriteLog("ON",time.strftime('%I:%M %p'), curtemp)
WriteLog("OFF",time.strftime('%I:%M %p'), curtemp)
