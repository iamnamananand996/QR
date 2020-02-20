import cv2
import numpy as np
from PIL import Image
import pytesseract

def readNumber(result):
	imname = "res.jpg"
	gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)	
	#print(type(imname))
	gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	#print(type(gray))
	cv2.imwrite(imname, gray)
	text = pytesseract.image_to_string(gray)
	text = text.split('\n')
	for line in text:
		words = line.split()
		for word in words:
			if word.isdigit() and len(word)==10:
				print(word)
				return word
			#outfile.write(word)

vc = cv2.VideoCapture(0)
	#'http://192.168.1.155:8080/video')


vc.release()
cv2.destroyAllWindows()