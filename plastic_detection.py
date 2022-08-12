#!/usr/bin/python3
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
import time

import jetson.inference
import jetson.utils
import keyboard
import numpy as np
import tkinter as tk

from gui import Application

# Once run variables
root = tk.Tk()

app = Application('assets/logo.jpeg',
        master=root,
        width=1280,
        height=1024,
        bg='white')

stream= True #True:camera|False:video or image

net = jetson.inference.detectNet(argv=['--model=mobilenetv1_models/own2-ssd-mobilenet.onnx',
    '--labels=mobilenetv1_models/Ownlabels.txt',
    '--input-blob=input_0',
    '--output-cvg=scores',
    '--output-bbox=boxes',
    '--threshold=0.4'])
net1 = jetson.inference.detectNet(argv=['--model=mobilenetv1_models/OWN-ssd-mobilenet.onnx',
    '--labels=mobilenetv1_models/OWNlabels.txt',
    '--input-blob=input_0',
    '--output-cvg=scores',
    '--output-bbox=boxes',
    '--threshold=0'])
net2 = jetson.inference.detectNet(argv=['--model=mobilenetv1_models/Own-ssd-mobilenet.onnx',
    '--labels=mobilenetv1_models/Ownlabels.txt',
    '--input-blob=input_0',
    '--output-cvg=scores',
    '--output-bbox=boxes',
    '--threshold=0.32'])
net3 = jetson.inference.detectNet(argv=['--model=mobilenetv1_models/own1-ssd-mobilenet.onnx',
    '--labels=mobilenetv1_models/Ownlabels.txt',
    '--input-blob=input_0',
    '--output-cvg=scores',
    '--output-bbox=boxes',
    '--threshold=0.5'])
net4 = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.2)
net5 = jetson.inference.detectNet(argv=['--model=mobilenetv1_models/TACO3-ssd-mobilenet.onnx',
    '--labels=mobilenetv1_models/TACOlabels.txt',
    '--input-blob=input_0',
    '--output-cvg=scores',
    '--output-bbox=boxes',
    '--threshold=0.4'])
net6 = jetson.inference.detectNet(argv=['--model=mobilenetv1_models/TACO4-ssd-mobilenet.onnx',
    '--labels=mobilenetv1_models/TACOlabels.txt',
    '--input-blob=input_0',
    '--output-cvg=scores',
    '--output-bbox=boxes',
    '--threshold=0.3'])

theNet = [net, net1, net2, net3, net4, net5, net6]

if stream:
    #800x600, 640x480, 1920x1080, 1280x960, 1280x720, 4096x2160, 1024x576
    camera = jetson.utils.gstCamera(1024, 576, "/dev/video0")
else:
    camera = jetson.utils.videoSource("assets/testing.jpg",argv=sys.argv)
    is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]
    output = jetson.utils.videoOutput("output_0.jpg",argv=sys.argv+is_headless)

#volatile variable
flag = 0
start = 0
randomOn = False
lang = 'b' #'b' -> Indonesian, 'v' -> English
last_lang = lang

def keyboardDetect():
    global flag, lang
    keys = [str(x) for x in range(0,len(theNet))] + ['esc']
    for key in (keys):
        if keyboard.is_pressed(key):
            try:
                flag = int(key)
            except:
                flag = -1
    
    if keyboard.is_pressed('b'):
        lang = 'b'
    elif keyboard.is_pressed('v'):
        lang = 'v'

def second():
    global theNet, last_lang, start, lang, stream, flag, camera, display
    
    if flag == -1 : exit()
    elif stream:
        fps=time.time()
        keyboardDetect()
        img, width, height = camera.CaptureRGBA()
        detections = theNet[flag].Detect(img, width, height)
        
        if len(detections) > 0 and flag == 0:
            start = time.time()
        
        if time.time()-start < 1 and flag == 0:
            timeOn = True
        else:
            timeOn = False
        
        if timeOn:
            if last_lang != lang:
                app.language(lang)
                last_lang = lang
            app.showReminder()
            #font.OverlayText(img, width, height, randomText, 0, height-64, font.White, font.Gray40)
            #font.OverlayText(img, width, height, str(start), 0, height-64, font.White, font.Black)
        
        #print(detections)
        #print(img.format)
        cuda_img = jetson.utils.cudaAllocMapped(width=width, height=height, format='rgba32f')
        jetson.utils.cudaMemcpy(cuda_img,img)
        array = jetson.utils.cudaToNumpy(cuda_img)
        array = array.astype(np.uint8)
        
        #display.RenderOnce(cuda_img, width, height)
        #display.SetTitle("Object Detection | Network {:.0f} FPS".format(detection.GetNetworkFPS()))
        app.once(array)
        app.language(lang)
        
        #print(detection.GetNetworkFPS())
        root.after(4,second)
        
    else:
        img = camera.Capture()
        detections = net.Detect(img, overlay="box,labels,conf") if flag else net2.Detect(img, overlay="box,labels,conf")
 
        print("detected {:d} objects in image".format(len(detections)))
        for detection in detections:
            print(detection)
        output.Render(img)
        if not camera.IsStreaming() or not output.IsStreaming():
            exit()

if __name__ == "__main__":
    second()
    root.mainloop()
