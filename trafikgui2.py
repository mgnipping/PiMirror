
import time
import requests
import json
import sys

if sys.platform.startswith('linux'):
    import ConfigParser
    from Tkinter import *
    config = ConfigParser.ConfigParser()

else:
    import configparser
    from tkinter import *
    config = configparser.ConfigParser()


max_items = 10
root = Tk()
labels = list()
label_clock = None
t = time.localtime()
api_trafiklab = ""

def requestData():
    
    #740001178 #huddinge sjukhus
    #740069445 #stortorp

    timearg = ""
    global t
    
    if t.tm_min != 59:
        timearg = "{0:0>2}:{1:0>2}".format(t.tm_hour, t.tm_min+1)
    else:
        timearg = "{0:0>2}:00".format((t.tm_hour+1)%24)  

    rstring = "https://api.resrobot.se/v2/departureBoard?key="+ api_trafiklab +"&id=740001178&time="+timearg+"&maxJourneys="+ str(max_items) +"&passlist=0&format=json"
    r = requests.get(rstring)

    data = r.json()
    departure = data.get("Departure")
    return departure

def initGUI():

    frame_clock = Frame(root, bg="black")
    frame_clock.grid(row= 0, column=0, padx=10, pady=10)
    frame_traffic = Frame(root, bg="black")
    frame_traffic.grid(row= 1, column=0, padx=10, pady=10)
    #frame_traffic.anchor("s")
    root.columnconfigure(0, weight = 1)
    root.rowconfigure(0, weight = 3)
    root.rowconfigure(1, weight = 1)
    #make window full screen
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    #suppress status bar, activity bar
    #root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()

    global labels
    for l in range(max_items*3):
        labels.append(Label(frame_traffic, text="", fg="white", bg="black", font="Helvetica 16 bold"))

    global label_clock
    label_clock = Label(frame_clock, text="00:00:00", fg="white", bg="black", font="Helvetica 40 bold")
    label_clock.grid()

    root.configure(background="black")
    for i in range(max_items):
        a = i*3
        labels[a].grid(row=i, column=0)
        labels[a+1].grid(row=i, column=1)   
        labels[a+2].grid(row=i, column=2, sticky=W)  


def updateGUI():

    departures = requestData()
    
    global max_items
    global labels
    for i in range(max_items):
        a = i*3

        deptime = departures[i].get("time")
        global t
        if (int(deptime[0:2]))<t.tm_hour+1 and (int(deptime[3:5])) <= t.tm_min:
            labels[a].configure(fg = "red")
            labels[a+1].configure(fg = "red")
            labels[a+2].configure(fg = "red")
        else:
            labels[a].configure(fg = "white")
            labels[a+1].configure(fg = "white")
            labels[a+2].configure(fg = "white")

        direction = departures[i].get("direction")
        indx = direction.find("(")
        if indx!=-1:
            direction = direction[:indx]
        
        labels[a].configure(text = deptime[:-3] + "|", font="Helvetica 16 bold" )   
        
        labels[a+1].configure(text = departures[i].get("name")[-3:] + "|" )   

        labels[a+2].configure(text = direction)
        #labels[a+2].configure(text = direction)
    

def updateClock():
    global label_clock
    global t
    t = time.localtime()
    if t.tm_sec == 0:
        updateGUI()
                
    label_clock.configure(text= time.strftime("%H:%M:%S",t))
    root.after(1000, updateClock)

def main():

    #run = True
    
    #create GUI
    initGUI()

    #get API keys from config file
    config.read('cdata.ini')
    global api_trafiklab
    api_trafiklab = str(config.get('API-keys','trafiklab1'))

    #request API data and update GUI
    updateGUI()
    updateClock()
    root.mainloop()

        
main()
