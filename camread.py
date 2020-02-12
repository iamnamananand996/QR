import cv2
import numpy as np
from PIL import Image
import pytesseract

vc = cv2.VideoCapture(0)
	#'http://192.168.1.155:8080/video')
imname = "res.jpg"
while True:
	ret, frame = vc.read()

	cv2.circle(frame, (200,200), 5, (0,0,255), -1)
	cv2.circle(frame, (620,200), 5, (0,0,255), -1)
	cv2.circle(frame, (200,320), 5, (0,0,255), -1)
	cv2.circle(frame, (620,320), 5, (0,0,255), -1)

	cv2.imshow("Frame", frame)

	result = frame[200:320, 200:620]
	
	#cv2.imshow("result", result)
	
	if cv2.waitKey(1) == ord('c'):
		cv2.imwrite(imname, result)
		break
	if cv2.waitKey(1) == ord('q'):
		break

gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
#print(type(imname))
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#print(type(gray))
text = pytesseract.image_to_string(gray)
text = text.split('\n')
with open('{}.txt'.format(imname.split('.')[0]), 'w+') as outfile:
	for word in text:
		if word.isdigit() and len(word)==10:
			print(word)
			outfile.write(word)

vc.release()
cv2.destroyAllWindows()