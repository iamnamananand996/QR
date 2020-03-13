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
import pytesseract
import re
from pytesseract import Output
import math
import numpy as np

    
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
            self.answer.insert(1, "Error occured")

    def execute(self,img):
        h, w = img.shape[:2]
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(img, 75, 150)
        lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength=50,maxLineGap=10)
        alist = []
        for line in lines:
            x1,y1,x2,y2 = line[0]
            #cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            if x2-x1 == 0:
                continue
            angle = round(math.atan((y2-y1)/(x2-x1)),1)
            #angle = angle*180/np.pi
            if abs(angle) < 0.1:
                text = pytesseract.image_to_string(img)
                #print(text)
                sens = text.split('\n')
                for sen in sens:
                    words = sen.split()
                    for word in words:
                        if word.isdigit() and len(word)==10:
                            #print(word+'\n')
                            return word
            if abs(angle) < 1 and abs(angle)>=0.1:
                if angle not in alist: 
                    alist.append(angle)
                    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 128), 1)
            for i in alist:
                M = cv2.getRotationMatrix2D((w/2,h/2), np.degrees(i), 1)
                fy = cv2.warpAffine(img, M, (w, h))

                text = pytesseract.image_to_string(fy)
                #print(text)
                sens = text.split('\n')
                for sen in sens:
                    words = sen.split()
                    for word in words:
                        if word.isdigit() and len(word)==10:
                            #print(word+'\n')
                            return word
        return ''

    def main(self, imag):
        #print(type(imag))
        #imag = cv2.imread(imag)
        imag = cv2.cvtColor(imag, cv2.COLOR_RGB2GRAY)
        #imag = cv2.threshold(imag, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        num_pattern = r'[0-9][0-9]+'
        data = pytesseract.image_to_data(imag, output_type=Output.DICT)
        #print(data['text'])
        img = imag.copy()
        n_boxes = len(data['text'])
        e = 200
        #print('f')
        for i in range(n_boxes):
            if int(data['conf'][i]) > 20:
                if re.match(num_pattern, data['text'][i]):
                    (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                    a = y-int(e/2) if y-int(e/2)>0 else 0
                    b = y+h+int(e/2) if y+h+int(e/2)<imag.shape[0] else imag.shape[0]
                    c = x-e if x-e>0 else 0
                    d = x+w+e if x+w+e<imag.shape[1] else imag.shape[1]
                    dup = imag[a:b, c:d]
                    #cv2.imshow('dup', dup)
                    #cv2.waitKey(0)
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    res = self.execute(dup)
                    if len(str(res))==10:
                        return res
        return ''

    def takeSnapshot(self):
        self.answer.delete('0', 'end')
        proimg = self.frame.copy()
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        
        p = os.path.sep.join((self.outputPath, filename))
        cv2.imwrite(p, proimg)
        img = cv2.imread(p)
        #print(type(img))
        text = self.main(img)
        #print("[INFO] saved {}".format(filename))
        if text is '':
            self.answer.insert(1, "no data found")
        else:
            self.answer.insert(1, text)

    def onClose(self):
        #print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()


#print("[INFO] warming up camera...")
vs = VideoStream().start()
pba = PhotoBoothApp(vs, "output")
pba.root.mainloop()
