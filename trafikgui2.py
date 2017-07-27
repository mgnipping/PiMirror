import time
import requests
import json
import configparser
from tkinter import *

max_items = 10
root = Tk()
labels = list()
api_trafiklab = ""

#GIT BRANCH LAYOUT

def requestData():

    rstring = "https://api.resrobot.se/v2/departureBoard?key="+ api_trafiklab +"&id=740001178&maxJourneys="+ str(max_items) +"&format=json"
    r = requests.get(rstring)

    data = r.json()
    departure = data.get("Departure")
    return departure

def initGUI():
    frame_traffic = Frame(root, bg="black")
    frame_traffic.grid(row= 1, column=0, padx=10, pady=10)
    frame_traffic.anchor("s")
    root.columnconfigure(0, weight = 1)
    root.rowconfigure(0, weight = 3)
    root.rowconfigure(1, weight = 1)
    #make window full screen
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    #suppress status bar, activity bar
    #root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()

    for l in range(max_items*3):
        labels.append(Label(frame_traffic, text="", fg="white", bg="black", font="Helvetica 16 bold"))

    root.configure(background="black")
    for i in range(max_items):
        a = i*3
        labels[a].grid(row=i, column=0)
        labels[a+1].grid(row=i, column=1)   
        labels[a+2].grid(row=i, column=2, sticky=W)  


def updateGUI(departures):

    for i in range(max_items):
        a = i*3
        labels[a].configure(text = departures[i].get("time")[:-3] + "|" )   
        #labels[a].grid(row=i, column=0)

        labels[a+1].configure(text = departures[i].get("name")[-3:] + "|" )   
        #labels[a+1].grid(row=i, column=1)

        labels[a+2].configure(text = departures[i].get("direction"))   
        #labels[a+2].grid(row=i, column=2, sticky=W)

    

def main():

    #create GUI
    initGUI()

    #get API keys from config file
    config = configparser.ConfigParser()
    config.read('cdata.ini')
    global api_trafiklab
    api_trafiklab = str(config.get('API-keys','trafiklab1'))

    #request API data and update GUI
    updateGUI(requestData())
    root.mainloop()
    

        
main()
