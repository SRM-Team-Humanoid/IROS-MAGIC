import cv2
import numpy as np


cap = cv2.VideoCapture(1)


y,u,v = 26,170,128

while True:

	_,img = cap.read()
	img_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
	
	blur = cv2.GaussianBlur(img_yuv,(7,7),2)
	median = cv2.medianBlur(blur ,5)

	die = cv2.inRange(blur, (np.array([y-45,u-30,v-30])), (np.array([y+45,u+30,v+30])))
	cv2.imshow("The Masked Image",die)
	
	outline,h = cv2.findContours(die,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	if len(outline)>0:	
		cnt = outline[0]
		epsilon = 0.1*cv2.arcLength(cnt,True)
		approx = cv2.approxPolyDP(cnt,epsilon,True)	

		'''im_floodfill = die.copy()
 		h, w = die.shape[:2]
		mask = np.zeros((h+2, w+2), np.uint8)
		cv2.floodFill(im_floodfill, mask, (0,0), 255);
    	'''
		oute = die.copy()
		#print approx[0][0][1]
		cv2.rectangle(oute, (approx[0][0][0],approx[0][0][1]),(approx[2][0][0],approx[2][0][1]),(255,255,0),1)
		cv2.imshow("Rectangle",oute)
		#cv2.drawContours(oute,approx,-1,(255,0,0),3)
		#cv2.imshow("Outline",oute)
		#fill = cv2.bitwise_not(im_floodfill)
	

		#cv2.imshow("Masked filled",fill)
 				#contours,hierarchy = cv2.findContours(fill,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
		#abc = cv2.drawContours(img, contours, -1, (0,0,255), 1)
		#cv2.imshow("",abc)
		#print len(contours)
	if cv2.waitKey(25)&0xff==27:
			break


