#!/usr/bin/env python3
import os
import schedule
import time, datetime
import requests
import urllib.request
from bs4 import BeautifulSoup

# changing working directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# getting prayer times 
def prayer_times():
    url = 'https://www.islamicfinder.org/world/united-states/5808079/redmond-prayer-times/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    x = soup.select('.prayertime')
    times = []
    for i in x:
        times.append(str(i)[25:-7])
    del times[1]
    return times

#the Doa playing function
def doa():
    os.system('mpg321 Doa.mp3 &')

#the Athan playing function
def athan():
    os.system('mpg321 Abdul-Basit.mp3 &')
    time.sleep(210)
    doa()

#playing an error message
def error():
    os.system('mpg321 Error.mp3')

#plays the Athan if it is the right time
def job():
    t = time.localtime()
    current_time = time.strftime("%I:%M %p", t)
    global ptime
    if current_time in ptime:
        athan()

# updates prayer times
def newday():
    global ptime
    while True:
        try:
            ptime = prayer_times()
            print("")
            print(datetime.datetime.now().strftime("%A" + " - " + "%x"))
            print(ptime)
            print("------------------------------------------------------------")
            print()
            break
        except:
            print("Error getting prayer times using the internet")
            error()

# getting prayer times when the app first start
while True:
    try:
        ptime = prayer_times()
        # startup indicator
        athan()
        print("")
        print(datetime.datetime.now().strftime("%A" + " - " + "%x"))
        print(ptime)
        print("------------------------------------------------------------")
        print()
        break
    except:
        print("Error getting prayer times using the internet")
        error()

# scheduling jobs...
schedule.every(1).minutes.do(job)
schedule.every().day.at("02:00").do(newday)

while True:
    schedule.run_pending()
    time.sleep(1)