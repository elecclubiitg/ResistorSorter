from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time
import math
from resistor_detection_with_mootor import run_motor
#time.sleep(10)

COLOR_BOUNDS = [
    #[(100,0,0) , (179,255,45) ,"BLACK", 0, (0,0,45)],
    [(1,0,0) , (15,255,255) ,"BROWN", 1, (0,51,102)],
    #[(20,0,0)    , (60,255,255) ,"GOLDEN",10,(0,15,255)],
    [(140,0,0) , (179,255,200),"RED" , 2 ,  (255,0,0)],
    #[(30,100,100)   ,(60,255,255), "ORANGE", 3, (0,128,52)],
    [(25, 95, 0) , (70, 255, 255)  , "YELLOW" , 4 , (0,255,255)   ],
    #[(90, 100, 100)  , (130, 255, 255)   , "GREEN"  , 5 , (0,255,0)     ], 
    [(130, 100, 100)    , (170, 255, 255)  , "BLUE"   , 6 , (255,0,0)     ], 
    [(170, 100, 100) , (179, 255, 255) , "PURPLE" , 7 , (255,0,127)   ], 
    #[(115, 55, 30)     , (160, 255, 55)   , "GRAY"   , 8 , (128,128,128) ], 
    # [(0, 0, 25)     , (119, 65, 255)  , "WHITE"  , 9 , (255,255,255) ],
]

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

while True:

    frame = picam2.capture_array()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cam = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    for i in COLOR_BOUNDS:
        color_mask = cv2.inRange(hsv,i[0],i[1])
        
        contours,hierarchy = cv2.findContours(color_mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            for c in contours:
                if cv2.contourArea(c) > 100 and cv2.contourArea(c) < 200:
                    x,y,w,h = cv2.boundingRect(c)
                    cv2.rectangle(cam,(x-w,y-h),(x+2*w,y+2*h),(0,0,255),1)
                    cv2.putText(cam,i[2],(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)




    cv2.imshow("frame",frame)
    cv2.imshow("HSV",hsv)
    cv2.imshow("camera",cam)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
time.sleep(0)
