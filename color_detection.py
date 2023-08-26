from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time


lower = np.array([20,40,120])
upper = np.array([60,255,255])


kernal = np.ones((20,20),np.uint8)

cv2.namedWindow("Trackbars")

def nothing(x):
    pass

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

while True:
    frame = picam2.capture_array()

    img1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
   

    mask = cv2.inRange(img,lower,upper)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernal)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernal)

    contours,hierarchy = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    frame = cv2.bitwise_and(frame,frame,mask=mask)


    output1 = mask
    output = mask
    h = 0
    w = 0

    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 100:
                x,y,w,h = cv2.boundingRect(contour)
                #cv2.circle(frame,(x,y),70,(0,0,255),1)
                cv2.rectangle(img1,(x-w,y-h),(x+2*w,y+2*h),(0,0,255),1)
                cv2.putText(img1,str(x),(x+w,y+h),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
                cv2.putText(img1,str(y),(x+w+20,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
                output = frame[y:y+h, x:x+w]


    if h > w :
        output = cv2.rotate(output,cv2.ROTATE_90_CLOCKWISE)
    

    output = cv2.resize(output,(400,200))

    frame = cv2.flip(output,1)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    

    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_range, upper_range)

    res = cv2.bitwise_and(frame, frame, mask=mask)
    res2 = cv2.cvtColor(res,cv2.COLOR_BGR2RGB)


    cv2.imshow("img",img1)
    cv2.imshow("hsv",hsv)
    cv2.imshow("mask",mask)
    cv2.imshow("res",res)
    cv2.imshow("res2",res2)
    cv2.imshow("output",output)
    cv2.imshow("output1",output1)
    


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
time.sleep(0)

