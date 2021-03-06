import cv2
import numpy as np


for i in range(1,5):
    try:
	cap = cv2.VideoCapture(i)
    except:
	continue
	pass
    break
if cap.isOpened() == False:
    print ("VideoCapture failed")

#y,u,v = 47,178,119
#y,u,v = 72,166,174
y,u,v = 63,155,130
kernel = np.array([3,3])
while True:
	ret,img = cap.read()

	img_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
	#kernel = np.ones((7,7),np.uint8)
	img_yuv = cv2.GaussianBlur(img_yuv,(7,7),2)
	#img_yuv = cv2.medianBlur(img_yuv ,3)
	#img_yuv = cv2.erode(img_yuv,kernel,20)
	img_yuv = cv2.morphologyEx(img_yuv, cv2.MORPH_OPEN, kernel)
	die = cv2.inRange(img_yuv, (np.array([y-45,u-30,v-30])), (np.array([y+45,u+30,v+30])))
	cv2.imshow("The Masked Image",die)
	im_floodfill = die.copy()
 	h, w = die.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	cv2.floodFill(im_floodfill, mask, (0,0), 255);


	fill = cv2.bitwise_not(im_floodfill)



	_,contours,hierarchy = cv2.findContours(fill,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
	#abc = cv2.drawContours(img, contours, -1, (0,0,255), 1)
	#cv2.imshow("",abc)
	count = min(len(contours),6)
	print count
	cv2.putText(fill,str(count), (50,300), cv2.FONT_HERSHEY_SIMPLEX, 5, (255,0,0))
	cv2.imshow("Masked filled",fill)
 	if cv2.waitKey(25)&0xff==27:
		break



	'''for cnt in contours:
    #if len(contours)>0:
        #c = max(contours, key=cv2.contourArea)

		x, y, w, h = cv2.boundingRect(cnt)
		cv2.rectangle(dilation,(x,y),(x+w,y+h),[255,0,0],2)
        #print x, y, w, h
	'''
