#!/usr/bin/env python3
import datetime
import os
import time
import requests
import schedule
from bs4 import BeautifulSoup
import pyttsx3
#import display
import tkinter as tk
from tkinter import Label, ttk

def updateDisplay(PTime, Index):
    # Figuring out the next salah time
    if Index == 0:
        Salah = "Fajer"
    elif Index == 1:
        Salah = "Doher"
    elif Index == 2:
        Salah = "Aser"
    elif Index == 3:
        Salah = "Magreb"
    else:
        Salah = "Isha"

    salah.config(text=Salah)
    salahTime.config(text=str(PTime))


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
        updateDisplay(ptime[location], location)

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

#start of program
root = tk.Tk()

# window title
root.title("Athan")

# window size
root.geometry('600x400')

#background color
root.configure(bg='black')

# label with a specific font
salah = ttk.Label(
    root,
    text="Salah",
    font=("Helvetica", 80),
    background="black", foreground="white")

salah.pack(ipadx=10, ipady=10)

# label with a specific font
salahTime = ttk.Label(
    root,
    text="Time",
    font=("Helvetica", 80),
    background="black", foreground="white")

salahTime.pack(ipadx=10, ipady=10)

# getting prayer times when the app first start
while True:
    try:
        # welcome message
        speak("Welcome!")
        # getting prayer times
        ptime = prayer_times()
        print("")
        print(ptime)
        t = time.localtime()
        # needs refactoring
        current_time = time.strftime("%I:%M %p", t)
        # finding the next Ptime
        if "AM" in str(t):
            if current_time > time.strptime(ptime[0], '%I:%M %p'):
                ntime=ptime[1]
                location=1
            else:
                ntime=ptime[0]
                location=0
                print("first else - AM")
        else:
            if current_time <= time.strptime(ptime[2], '%I:%M %p'):
                ntime=ptime[2]
                location=2
            elif current_time <= time.strptime(ptime[3], '%I:%M %p'):
                ntime=ptime[3]
                location=3
            elif current_time <= time.strptime(ptime[4], '%I:%M %p'):
                ntime=ptime[4]
                location=4
            else:
                ntime=ptime[0]
                location=0
                print("second else")

        updateDisplay(ntime, location)
        print(str(ptime[2]) + " -- " + str(current_time) + "--" + str(current_time <= ptime[1]))
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
    root.update()

# keep the window displaying
root.mainloop()