import datetime as dt

import tkinter as tk
import cv2

import PIL.Image as imgg
import PIL.ImageTk as imgk

from random_message import Reminder

class Application(tk.Canvas):
    def __init__(self, *args, **kwargs):
        self.logoPath = args[0]
        
        self.WIDTH = kwargs['width']
        self.HEIGHT = kwargs['height']
        
        self.lang = 'b'
        self.last_lang = self.lang
        self.flag = self.galf = self.showing = True
        self.thanks = False
        
        self.reminder = Reminder()
        
        self.randomText = self.reminder.getRandom(self.lang) 
    
        # Initializing GUI
        super().__init__(**kwargs)
        self.pack()

        self.master.attributes("-fullscreen", True)
        
        self.date = tk.Label(self, text = dt.datetime.now().strftime("%I"),
                bg='white', font="Helvetica 32 bold")
        self.Time = tk.Label(self, text = dt.datetime.now().strftime("%I"),
                bg='white', font="Helvetica 56 bold")
        self.Llogo = tk.Label(self,bg='white')
        self.gambar = tk.Label(self)
        self.randomMessage = tk.Label(self,text=self.randomText, 
                font="Helvetica 32 bold")
        
        # Create Canvas Window
        self.create_window(self.WIDTH*0.5, self.HEIGHT*0.5,
                window=self.gambar, anchor='center')
        self.create_window(128, self.HEIGHT*0.09,
                window=self.Llogo, anchor='nw')
        self.canvasLabel = self.create_window(self.WIDTH*0.5,
                self.HEIGHT*0.9, window=self.randomMessage,
                anchor='center',state='hidden')
        self.canvasDate = self.create_window(1152, 
                self.HEIGHT*0.07, window=self.date, anchor='e')
        self.canvasTime = self.create_window(1152, 
                self.HEIGHT*0.1, window=self.Time, anchor='ne')
        
        # Logo
        self.logo = cv2.cvtColor(cv2.imread(self.logoPath),cv2.COLOR_BGR2RGBA)

        scale = 0.2
        self.logo = cv2.resize(self.logo,(int(1500*scale),int(600*scale)))
        imgtk = self.capture(self.logo)
        self.Llogo.imgtk = imgtk
        self.Llogo.configure(image = imgtk) 
        
        #start the loop
        if __name__ == "__main__":
            self.vid = cv2.VideoCapture('/dev/video0')
            self.loop()
            self.mainloop()

    def showThankyou(self):
        self.thanks = True

    def _showThankyou(self):
        if self.thanks:
            if self.flag:
                self.randomMessage.config(text='Thankyou :)')
                self.itemconfig(self.canvasLabel, state = "normal")
                self.flag = False
                #self.galf = True
        else:
            self.randomMessage.config(text='Silakan sukarela foto sampah plastik yang\ndapat di "Reuse" sebanyak-banyaknya\nPress (Space)')
            self.itemconfig(self.canvasLabel, state = "normal")
            self.flag = True
                #self.galg = False

    def showGrid(self):
        self.create_line(self.WIDTH*0.3333,0,self.WIDTH*0.3333,self.HEIGHT, fill="green", width=5)
        self.create_line(self.WIDTH*0.6666,0,self.WIDTH*0.6666,self.HEIGHT, fill="green", width=5)
        self.create_line(0,self.HEIGHT*0.3333,self.WIDTH,self.HEIGHT*0.3333, fill="green", width=5)
        self.create_line(0,self.HEIGHT*0.6666,self.WIDTH,self.HEIGHT*0.6666, fill="green", width=5)

    def clock(self):
        hari = dt.datetime.now().strftime("%a")
        if self.lang == 'b':
            hari = 'Senin' if hari == "Mon" else \
                'Selasa' if hari == "Tue" else \
                'Rabu' if hari == "Wed" else \
                'Kamis' if hari == "Thu" else \
                'Jumat' if hari == "Fri" else \
                'Sabtu' if hari == "Sat" else \
                'Minggu' if hari == "Sun" else hari
        self.Time.config(text = dt.datetime.now().strftime("%H:%M:%S"))
        self.date.config(text = hari + dt.datetime.now().strftime(", %d %b %Y"))
    def mainloop(self):
        self.master.mainloop()

    def capture(self, camFeed):
        #camFeed = cv2.cvtColor(camFeed, cv2.COLOR_BGR2RGBA)
        img = imgg.fromarray(camFeed)
        imgtk = imgk.PhotoImage(img)
        return imgtk

    def language(self, lang):
        self.lang = lang
    
    def loop(self, camFeed=None, takeData=False):
        if __name__ == '__main__':
            ret, camFeed = self.vid.read()
        if takeData:
            self._showThankyou()
        self._showReminder()
        self.clock()
        self.showing = self.thanks = False
        imgtk=self.capture(camFeed)
        self.gambar.imgtk = imgtk
        self.gambar.configure(image=imgtk)
        self.master.after(1,self.loop)

    def once(self, camFeed=None, takeData=False):
        if __name__ == '__main__':
            ret, camFeed = self.vid.read()
        self._showReminder()
        if takeData:
            self._showThankyou()
        self.clock()
        self.showing = self.thanks = False
        imgtk=self.capture(camFeed)
        self.gambar.imgtk = imgtk
        self.gambar.configure(image=imgtk)
    
    def showReminder(self):
        self.showing = True

    def _showReminder(self):
        if self.showing:
            if self.flag:
                self.reminder.randomIndex()
            if self.flag or self.last_lang != self.lang:
                self.randomMessage.config(
                        text=self.reminder.getRandomIndexed(self.lang))
                self.itemconfig(self.canvasLabel,state="normal")
                self.last_lang = self.lang
                self.flag = False
                self.galf = True
        else:
            if self.galf:
                self.itemconfig(self.canvasLabel,state="hidden")
                self.flag = True
                self.galf = False
    
if __name__ == "__main__":
    app = Application("assets/logo.jpeg",master=tk.Tk(),width=1280,height=1024,bg='white')
