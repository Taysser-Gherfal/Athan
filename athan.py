#!/usr/bin/env python3
import os
import schedule
import time
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

#the Athan playing function
def athan():
    os.system('mpg321 Abdul-Basit.mp3 &')

#plays the Athan if it is the right time
def job():
    t = time.localtime()
    current_time = time.strftime("%I:%M %p", t)
    print(current_time) # to be removed
    global ptime
    print(ptime) # to be removed
    if current_time in ptime:
        athan()

# updates prayer times
def newday():
    global ptime
    try:
        ptime = prayer_times()
    except:
        print("Error getting prayer times using the internet")
    #ptime.append("04:02 PM") # to be removed
    print("newday:") # to be removed
    print(ptime) # to be removed

# startup indicator
athan()

# getting prayer times when the app first start
try:
    ptime = prayer_times()
except:
    print("Error getting prayer times using the internet")

# scheduling jobs...
schedule.every(1).minutes.do(job)
schedule.every().day.at("02:00").do(newday)

while True:
    schedule.run_pending()
    time.sleep(1)