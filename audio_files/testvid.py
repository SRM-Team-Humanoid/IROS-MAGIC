import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while True:
    img = cap.read()
    #cv2.imshow('hello',img)
    print img