from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time
import math
from resistor_detection_with_mootor import run_motor
#time.sleep(10)

def find_hsv(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        h,s,v = sharpen[y,x]
        print("H: ",h)
        print("S: ",s)
        print("V: ",v)

lower = np.array([20,40,120])
upper = np.array([60,255,255])

golden_lower = np.array([16,00,1])
golden_upper = np.array([35,255,225])

sharpen_kernal = np.ones((5,5),np.float32)/25


kernal = np.ones((20,20),np.uint8)

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

COLOR_BOUNDS = [
    [(1,0,0) , (179,100,50) ,"BLACK", 0, (0,0,45)],
    [(7,0,0) , (15,255,255) ,"BROWN", 1, (0,51,102)],
    #[(16,0,0)    , (35,255,255) ,"GOLDEN",10,(0,15,255)],
    [(1,0,0) , (5,255,255),"RED" , 2 ,  (255,0,0)],
    [(140,0,0) , (179,255,255),"RED" , 2 ,  (255,0,0)],
    [(16,150,226)   ,(30,255,255), "ORANGE", 3, (0,128,52)],
    [(31, 95, 0) , (50, 255, 255)  , "YELLOW" , 4 , (0,255,255)   ],
    [(50, 170, 00)  , (80, 255, 255)   , "GREEN"  , 5 , (0,255,0)     ], 
    [(100, 00, 220)    , (140, 255, 255)  , "BLUE"   , 6 , (255,0,0)     ], 
    [(100, 00, 00) , (140, 255, 200) , "PURPLE" , 7 , (255,0,127)   ], 
    #[(115, 55, 30)     , (160, 255, 55)   , "GRAY"   , 8 , (128,128,128) ], 
    # [(0, 0, 25)     , (119, 65, 255)  , "WHITE"  , 9 , (255,255,255) ],
]

while True:
    frame = picam2.capture_array()
    run_motor(50,100)


    img1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)          #to convert original image
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
   

    mask = cv2.inRange(img,lower,upper)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernal)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernal)

    contours,hierarchy = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    frame = cv2.bitwise_and(frame,frame,mask=mask)

    h = 0
    w = 0
    output = mask
    output2 = mask

    # frame = cv2.bitwise_and(frame,frame,mask=mask)


    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                time.sleep(2)
                x,y,w,h = cv2.boundingRect(contour)
                if y < 90 or y > 180:
                    angle = int((y-135)/4.2)
                    run_motor(angle,50)
                cv2.rectangle(img1,(x-w,y-h),(x+2*w,y+2*h),(0,0,255),1)
                #cv2.circle(frame,(x,y),70,(0,0,255),1)
                
    #cv2.imshow("IMGRESISTOR",sharpen_

                
                    
                l = x + w
                g = y + h
                
                output = frame[y:y+h, x:x+w]

    if h > w :
        output = cv2.rotate(output,cv2.ROTATE_90_CLOCKWISE)     
  
    output = cv2.resize(output,(720,360))
    output = cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
    kernal_25 = np.ones((10,10),np.float32)/625.0

    #sharpen_bgr = cv2.filter2D(output,-1,kernal_25)

    #out.write(sharpen_bgr)

    sharpen = cv2.cvtColor(output,cv2.COLOR_BGR2HSV)

    cv2.namedWindow('sharpen')

    cv2.setMouseCallback('sharpen',find_hsv)

    # golden_lower = np.array([125,50,0])
    # golden_upper = np.array([145,255,78])
    golden_kernal = np.ones((20,20),np.uint8)

    golden_mask = cv2.inRange(sharpen,golden_lower,golden_upper)
    golden_mask = cv2.morphologyEx(golden_mask,cv2.MORPH_CLOSE,golden_kernal)
    golden_mask = cv2.morphologyEx(golden_mask,cv2.MORPH_OPEN,golden_kernal)

    golden_contours,golden_hierarchy = cv2.findContours(golden_mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    

    if len(golden_contours) != 0:
        for contour in golden_contours:
            if cv2.contourArea(contour) > 5000:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(output,(x,y),(x+w,y+h),(0,0,255),1)
                #cv2.circle(frame,(x,y),70,(0,0,255),1)
                # cv2.putText(output,str(x),(x+w,y+h),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)

                if x < 360:
                    sharpen = cv2.flip(sharpen,1)
                    output = cv2.flip(output,1)

    
    bands = []
    


    for i in COLOR_BOUNDS:
        color_mask = cv2.inRange(sharpen,i[0],i[1])
        color_mask = cv2.morphologyEx(color_mask,cv2.MORPH_CLOSE,golden_kernal)
        color_mask = cv2.morphologyEx(color_mask,cv2.MORPH_OPEN,golden_kernal)

        color_contours,color_hierarchy = cv2.findContours(color_mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        area_max = 0
        no_band = 0
        

        if len(color_contours) != 0:
            for contour in color_contours:
                if cv2.contourArea(contour) > 5000:
                    x,y,w,h = cv2.boundingRect(contour)
                    cv2.rectangle(output,(x,y),(x+w,y+h),(0,0,255),1)
                    area_max = cv2.contourArea(contour)
                    cv2.putText(output,i[2],(x+w,y+h),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
                    #cv2.putText(output,str(cv2.contourArea(contour)),(x+w,y+h),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)

                    #cv2.putText(output,str(x),(x+w,y+h),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
                    # cv2.putText(output,str(y),(x+w+10,y+h+10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
                    #cv2.putText(output,str(i[3]),(x+w,y+h),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
                    bands.append([i[3],x])
                    no_band += 1

                    for j in bands:
                        if j[0] == i[3] & x != j[0] & abs(x-j[0]) > 2*h:
                            bands.append((i[3],x))

    for i in range(0,len(bands)):
        for j in range(0,len(bands)-i-1):
            if bands[j][1] > bands[j+1][1]:
                temp = bands[j]
                bands[j] = bands[j+1]
                bands[j+1] = temp



    if len(bands) == 3:
        resistance = (bands[0][0]*10 + bands[1][0])*(math.pow(10,bands[2][0]))
        cv2.putText(img1,str(resistance),(l,g+100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
        if resistance >= 22001:
            run_motor(-1600,500)
        else :
            run_motor(1600,500)
    



    cv2.imshow("mask1",mask)
    cv2.imshow("webcam",frame)
    cv2.imshow("img",img1)
    cv2.imshow("HSV",img)
    cv2.imshow("output",output)
    cv2.imshow("output2",output2)
    cv2.imshow("sharpen",sharpen)
    cv2.imshow("golden",golden_mask)
    #cv2.imshow("IMGRESISTOR",sharpen_bgr)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
time.sleep(0)


