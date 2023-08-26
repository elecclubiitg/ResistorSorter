from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time
import math
from resistor_detection_with_mootor import run_motor

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

# Define the lookup table for resistor colors and their corresponding values
resistor_colors = {'black':0, 'brown':1, 'red':2, 'orange':3, 'yellow':4,
                   'green':5, 'blue':6, 'violet':7, 'gray':8, 'white':9}


# Define the color ranges for each resistor band (in HSV format)
color_ranges = [(0, 0, 0), (15, 255, 255), (0, 255, 255), (15, 255, 255), 
                (20, 255, 255), (45, 255, 255), (100, 255, 255), (140, 255, 255), 
                (0, 0, 128), (0, 0, 255)]

while True:
    # Load the image and convert to HSV color space
    img = picam2.capture_array()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Use the color ranges to threshold the image and find the contours of each color band
    contours = []
    for i in range(3):  # Assumes a three-band resistor
        mask = cv2.inRange(hsv, color_ranges[i*2], color_ranges[i*2+1])
        _, cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours.append(cnts[0])

    # Sort the contours by x-coordinate to determine the order of the color bands
    contours.sort(key=lambda c: cv2.boundingRect(c)[0])

    # Get the value of each color band and combine to obtain the total resistance
    resistance = 0
    for c in contours:
    # Determine the color of the current band
        color_mask = cv2.bitwise_and(hsv, hsv, mask=cv2.inRange(hsv, cv2.minEnclosingCircle(c)[0], cv2.minEnclosingCircle(c)[0]))
        h, s, v = cv2.split(color_mask)
        h_mean = cv2.mean(h)[0]
        s_mean = cv2.mean(s)[0]
        v_mean = cv2.mean(v)[0]
        color = min(resistor_colors, key=lambda x: abs(h_mean - color_ranges[resistor_colors[x]*2][0]))

    # Determine the value of the current band
    resistance += resistor_colors[color] * 10**(len(contours)-contours.index(c)-1)

    print("Resistance value: {} ohms".format(resistance))

    cv2.imshow("img",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
time.sleep(0)

