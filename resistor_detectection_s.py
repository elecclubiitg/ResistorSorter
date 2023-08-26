from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time
import math


def isResistor(frame):
    img1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    cv2.imshow("cam",img1)
    cv2.imshow("hsv",img)

    

