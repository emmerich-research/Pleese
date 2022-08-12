import os
import time

import datetime as dt
from pynput import keyboard
import tkinter as tk
import cv2

from GUI import Application

# Make directory
first = os.getcwd()
try:
    os.chdir('JPEGImages')
except:
    os.mkdir('JPEGImages')
os.chdir(first)

root = tk.Tk()
app = Application(master=root, width=1920, height=1080, bg='white')

cam = cv2.VideoCapture("/dev/video0")

take = False
flag = True

def checkKey(key):
    global take
    try:
        if key == keyboard.Key.space:
            take = True
    except AttributeError:
        pass

def releaseKey(key):
    global take
    take = False
    #print(key._from_symbol())
    #print(type(key._from_symbol))
    #if key == keyboard.a:
    #    print('ok')
    #print(type(key))
    #oot.bind('a', lambda x:print('a'))
    #if keyboard.is_pressed("space"):
    #    take = True
#while True:
start = 0
def mainLoop():
    global take, flag, start
    
    ret, frame = cam.read()

   #checkKey()
    if take:
        if flag:
            Timetake = dt.datetime.now().strftime("JPEGImages/%Y%m%d-%H%M%S.jpg")
            cv2.imwrite(Timetake, frame)
            start = time.time()
            flag = False
    else:
        flag = True
    if (time.time()-start)<3:
        app.showThankyou()


    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    app.loop(frame,True)
    root.after(1,mainLoop)

#Blocking
#with keyboard.Listener(on_press=checkKey(),
#        on_release=on_release) as listener:
#    listener.join()

#Non Blocking
listener = keyboard.Listener(on_press=checkKey, on_release=releaseKey)
listener.start()

mainLoop()
root.mainloop()
