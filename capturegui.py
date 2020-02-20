from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style, Label
import camread_u
import cv2
import numpy as np
from PIL import Image

number = '0'


def captureFrame(state=True):
	vc = cv2.VideoCapture(0)
	while True:
		ret, frame = vc.read()
		cv2.imshow("Frame", frame)
		#readNumber(frame)
		imname = "res.jpg"
		if state==True:
			number = camread_u.readNumber(frame)
			break

		

def main():

	root = Tk()
	root.geometry("300x200+300+300")
	root.title("Buttons")
	style = Style()
	style.theme_use("default")

	okButton = Button(root, text="Scan", command = captureFrame)
	okButton.pack()

	closeButton = Button(root, text="Close", command = quit)
	closeButton.pack(padx=5, pady=5)
	
	num = Label(root, text=number)
	num.pack()
	root.mainloop()


if __name__ == '__main__':
	main()