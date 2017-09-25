import cv2
import numpy as np

def nothing(x):
	pass

buffer = [0,0,0,0,0,0,0,0,0,0,0,0,0]

try:
	with open("calib.txt",'r') as f:
		vals = f.readline()
		vals = map(int,vals.split())
except:
	 	vals = [0,0,0]

print vals
raw_input(">")


def counter(val):
	global buffer
	buffer = buffer[1:]
	buffer.append(val)
	count = int(round(sum(buffer)/float(len(buffer)+1)))
	cv2.putText(fill,str(count), (50,300), cv2.FONT_HERSHEY_SIMPLEX, 5, (255,0,0))
	with open("x.txt",'w') as f:
		f.write(str(count))


# Create a black image, a window
img = np.zeros((300,300,3), np.uint8)
cv2.namedWindow('image')
# create trackbars for color changeh
cv2.createTrackbar('Y','image',0,255,nothing)
cv2.createTrackbar('U','image',0,255,nothing)
cv2.createTrackbar('V','image',0,255,nothing)
cv2.setTrackbarPos('Y','image',vals[0])
cv2.setTrackbarPos('U','image',vals[1])
cv2.setTrackbarPos('V','image',vals[2])
cap = cv2.VideoCapture(0)
cv2.createTrackbar('Blurring','image',10,30,nothing)
cap = cv2.VideoCapture(1)
while True:
	y = cv2.getTrackbarPos('Y','image')
	u = cv2.getTrackbarPos('U','image')
	v = cv2.getTrackbarPos('V','image')
	vals = [y,u,v]
	sigma = cv2.getTrackbarPos('Blurring','image')
	sigma = sigma/10
	img[:] = [y,u,v]
	img= cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
	_,f = cap.read()
	img_yuv = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)
	img_yuv = cv2.GaussianBlur(img_yuv, (7, 7), sigma)
	img_yuv = cv2.morphologyEx(img_yuv, cv2.MORPH_OPEN, (7,7))
	die = cv2.inRange(img_yuv, (np.array([y-45,u-30,v-30])), (np.array([y+45,u+30,v+30])))
	cv2.imshow("The Masked Image",die)
	im_floodfill = die.copy()
	h, w = die.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	cv2.floodFill(im_floodfill, mask, (0,0), 255);
	fill = cv2.bitwise_not(im_floodfill)
	_,contours,hierarchy = cv2.findContours(fill,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
	count = min(len(contours),6)
	counter(count)

	cv2.imshow("Masked filled",fill)
 	if cv2.waitKey(25)&0xff==27:
		break
with open("calib.txt",'w') as f:
	f.write(" ".join(map(str,vals)))
cap.release()
cv2.destroyAllWindows()
