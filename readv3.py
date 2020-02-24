import cv2
import re
import pytesseract
from pytesseract import Output
import math
import numpy as np

def execute(image, center = None, scale = 1.0):
	#if center is None:
	#	center = (w / 2, h / 2)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	"""	
	edges = cv2.Canny(gray, 75, 150)
	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=250)
	for line in lines:
		x1, y1, x2, y2 = line[0]
		angle = math.atan((y2-y1)/(x2-x1))
	M = cv2.getRotationMatrix2D(center, angle, scale)
	gray = cv2.warpAffine(image, M, (w, h))
	"""	
	
	text = pytesseract.image_to_string(gray)
	#print(text)
	lines = text.split('\n')
	for line in lines:
		words = line.split()
		for word in words:
			if word.isdigit() and len(word)==10:
				#print(word+'\n')
				return word
	

imag = cv2.imread('images/25.jpg')
date_pattern = r'[0-9]+'
d = pytesseract.image_to_data(imag, output_type=Output.DICT)
img = imag.copy()
n_boxes = len(d['text'])
e = 200

for i in range(n_boxes):
	if int(d['conf'][i]) > 20:
		if re.match(date_pattern, d['text'][i]):
			(x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
			a = y-int(e/2) if y-int(e/2)>0 else 0
			b = y+h+int(e/2) if y+h+int(e/2)<imag.shape[0] else imag.shape[0]
			c = x-e if x-e>0 else 0
			f = x+w+e if x+w+e<imag.shape[1] else imag.shape[1]
			dup = imag[a:b, c:f]
			#cv2.imshow('dup', dup)
			#cv2.waitKey(0)
			img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
			word = execute(dup)
			if word!='':
				print(word)
				break


#cv2.imshow('img', img)
#cv2.waitKey(0)
