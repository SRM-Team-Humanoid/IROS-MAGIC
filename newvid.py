import cv2
import numpy as np

cap= cv2.VideoCapture(0)

while True:
	ret,img = cap.read()
	cv2.imshow("DFW",img)
	
	if cv2.waitKey(25)&0xff==27:
		break
