from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time

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

    frame = cv2.flip(frame,1)
    frame2 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame3 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(frame3,(3,3),0)
    edges = cv2.Canny(blur,254,255)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    contours,hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    output = frame2.copy()
    cv2.drawContours(output,contours,-1,(0,255,0),2)

    

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
    res = cv2.cvtColor(res,cv2.COLOR_BGR2RGB)
    res2 = res[0:720,120:520]


    cv2.imshow("img",frame)
    cv2.imshow("img2",frame2)
    cv2.imshow("img3",frame3)
    cv2.imshow("hsv",hsv)
    cv2.imshow("mask",mask)
    cv2.imshow("res",res)
    cv2.imshow("res2",res2)
    cv2.imshow("object",output)
    


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
time.sleep(0)

