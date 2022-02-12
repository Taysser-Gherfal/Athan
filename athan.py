#!/usr/bin/env python3
import datetime
import os
import time
import requests
import schedule
from bs4 import BeautifulSoup
import pyttsx3
import display

# setting voice rate
engine = pyttsx3.init()
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 150)     # setting up new voice rate

# changing working directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# speaking
def speak(text):
    engine.say(text)
    engine.runAndWait()

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

# the Doa playing function
def doa():
    os.system('mpg321 Doa.mp3 &')

# the Athan playing function
def athan():
    os.system('mpg321 Abdul-Basit.mp3 &')
    time.sleep(210)
    doa()

# playing an intro
def intro():
    os.system('mpg321 Intro.mp3 &')

# plays the Athan if it is the right time
def job():
    t = time.localtime()
    current_time = time.strftime("%I:%M %p", t)
    global ptime
    if current_time in ptime:
        athan()
        location = ptime.index(current_time)
        # info about the next prayer time
        location = location + 1
        if location > 4:
            location = 0
        display.updateDisplay(ptime[location], location)

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
            speak("I'm unable to get your prayer times from the internet! Please check or configure your internet connection")
            time.sleep(60)

# getting prayer times when the app first start
while True:
    try:
        # welcome message
        speak("Welcome!")
        # getting prayer times
        ptime = prayer_times()
        print("")
        print(datetime.datetime.now().strftime("%A" + " - " + "%x"))
        print(ptime)
        display.updateDisplay()
        print("------------------------------------------------------------")
        print()
        # startup indicator
        intro()
        break
    except:
        print("Error getting prayer times using the internet")
        speak("I'm unable to get your prayer times from the internet! Please check or configure your internet connection")
        time.sleep(60)

# scheduling jobs...
schedule.every(1).minutes.do(job)
schedule.every().day.at("02:00").do(newday)

while True:
    schedule.run_pending()
    time.sleep(1)
