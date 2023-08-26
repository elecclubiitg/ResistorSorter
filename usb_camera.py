import cv2
import numpy as np

lower = np.array([6,97,71])
upper = np.array([97,255,255])


cap = cv2.VideoCapture(-1)

kernal = np.ones((10,10),np.uint8)

while(True):
    ret,frame = cap.read()

    img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(img,lower,upper)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernal)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernal)

    contours,hierarchy = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 100:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.circle(frame,(x,y),70,(0,0,255),1)
                #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
    

    # output = cv2.drawContours(frame,contours,-1,(0,0,255),1)
    # output2 = cv2.drawContours(frame,contours2,-1,(0,0,255),1)

    

    cv2.imshow("mask1",mask)
    cv2.imshow("webcam",frame)
    cv2.imshow("HSV",img)
    # cv2.imshow("output",output)
    # cv2.imshow("output2",output2)

    cv2.waitKey(1)