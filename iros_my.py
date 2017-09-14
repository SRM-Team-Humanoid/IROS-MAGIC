import cv2
import numpy as np



cap = cv2.VideoCapture(1)


y,u,v = 60,176,117


while True:
	_,img = cap.read()
	img_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
	die = cv2.inRange(img_yuv, (np.array([y-45,u-30,v-30])), (np.array([y+45,u+30,v+30])))
	cv2.imshow("The Masked Image",die)
	im_floodfill = die.copy()
 	h, w = die.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	cv2.floodFill(im_floodfill, mask, (0,0), 255);
 
    
	fill = cv2.bitwise_not(im_floodfill)
	cv2.imshow("Masked filled",fill)
 	if cv2.waitKey(25)&0xff==27:
		break

	'''contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
	if cv2.waitKey(25)&0xff==27:
		break
	'''	