from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time

lower = np.array([0,99,0])
upper = np.array([179,255,255])

kernal = np.ones((7,7),np.uint8)

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()



while True:
    frame = picam2.capture_array()


    img1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
   

    mask = cv2.inRange(img,lower,upper)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernal)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernal)

    mask = cv2.inRange(img,lower,upper)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernal)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernal)

    contours,hierarchy = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 100:
                x,y,w,h = cv2.boundingRect(contour)
                #cv2.circle(frame,(x,y),70,(0,0,255),1)
                cv2.rectangle(img1,(x-w,y-h),(x+2*w,y+2*h),(0,0,255),1)
                output = frame[y:y+h, x:x+w]


    if h > w :
        output = cv2.rotate(output,cv2.ROTATE_90_CLOCKWISE)
    

    output = cv2.resize(output,(400,200))

    kernal_25 = np.ones((25,25),np.float32)/625.0

    #sharpen_bgr = cv2.filter2D(output,-1,kernal_25)

    #out.write(sharpen_bgr)

    sharpen = cv2.cvtColor(output,cv2.COLOR_BGR2HSV)

    golden_lower = np.array([125,50,0])
    golden_upper = np.array([145,255,78])
    golden_kernal = np.ones((7,7),np.uint8)

    golden_mask = cv2.inRange(sharpen,golden_lower,golden_upper)
    golden_mask = cv2.morphologyEx(golden_mask,cv2.MORPH_CLOSE,golden_kernal)
    golden_mask = cv2.morphologyEx(golden_mask,cv2.MORPH_OPEN,golden_kernal)

    golden_contours,golden_hierarchy = cv2.findContours(golden_mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    area_max = 0

    if len(golden_contours) != 0:
        for contour in golden_contours:
            if area_max < cv2.contourArea(contour) :
                x,y,w,h = cv2.boundingRect(contour)
                #cv2.circle(frame,(x,y),70,(0,0,255),1)
                cv2.rectangle(output,(x,y),(x+w,y+h),(0,0,255),1)
                area_max = cv2.contourArea(contour)

    
                


    cv2.imshow("mask1",mask)
    #cv2.imshow("webcam",frame)
    cv2.imshow("img",img1)
    cv2.imshow("HSV",img)
    cv2.imshow("output",output)
    cv2.imshow("sharpen",sharpen)
    cv2.imshow("golden",mask)
    #cv2.imshow("IMGRESISTOR",sharpen_bgr)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
time.sleep(0)

