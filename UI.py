from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
from imutils.video import VideoStream, WebcamVideoStream
import time
import argparse
import pytesseract


class PhotoBoothApp:
    def __init__(self, vs, outputPath):
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.root = tki.Tk()
        self.panel = None

        btn_1 = tki.Button(self.root, text="Sticker Image",
                           command=self.takeSnapshot)
        btn_1.grid(row=0, column=1, padx=10, pady=30)

        btn_2 = tki.Button(self.root, text="Hand Written Image",
                           command=self.takeSnapshot)
        btn_2.grid(row=0, column=2, padx=10, pady=20)

        textDataLebel = tki.Label(
            self.root, text="Extrated Data", font=('bold', 14))
        textDataLebel.grid(row=1, column=0)

        self.answer = tki.Listbox(self.root, height=4, width=80)
        self.answer.grid(row=2, column=0, padx=10, pady=20)
        # answer.insert(1, "9663077540")

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.root.wm_title("PyImageSearch PhotoBooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        try:

            while not self.stopEvent.is_set():

                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=500)

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.grid(row=0, column=0, padx=10, pady=10)

                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self):
        self.answer.delete('0', 'end')
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        # print("Output", self.frame.copy())
        # print("Type", type(self.frame.copy()))
        img = Image.open("2.png")
        text = pytesseract.image_to_string(self.frame.copy())
        print("answer", text)
        p = os.path.sep.join((self.outputPath, filename))

        # save the file
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}{}".format(filename, p))
        if text is '':
            self.answer.insert(1, "no data found")
        else:
            self.answer.insert(1, text)

    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()


print("[INFO] warming up camera...")
vs = VideoStream().start()
pba = PhotoBoothApp(vs, "output")
pba.root.mainloop()
