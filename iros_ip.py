import cv2
import numpy as np

def eyes(cap, y = 75,u = 179,v = 147):
	_,img = cap.read()
	img_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)

	blur = cv2.GaussianBlur(img_yuv,(7,7),1.3)
	median = cv2.medianBlur(blur ,5)

	die = cv2.inRange(blur, (np.array([y-45,u-30,v-30])), (np.array([y+45,u+30,v+30])))
	cv2.imshow("The Masked Image",die)
	im_floodfill = die.copy()
	h, w = die.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	cv2.floodFill(im_floodfill, mask, (0,0), 255)
 

	fill = cv2.bitwise_not(im_floodfill)
	

	cv2.imshow("Masked filled",fill)
	if cv2.waitKey(25)&0xff==27:
		return

	contours,hierarchy = cv2.findContours(fill,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
	#abc = cv2.drawContours(img, contours, -1, (0,0,255), 1)
	#cv2.imshow("",abc)
	return len(contours)
	'''for cnt in contours:
	#if len(contours)>0:
		#c = max(contours, key=cv2.contourArea)

		x, y, w, h = cv2.boundingRect(cnt)
		cv2.rectangle(dilation,(x,y),(x+w,y+h),[255,0,0],2)
		#print x, y, w, h
	'''
