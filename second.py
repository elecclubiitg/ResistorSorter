from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

while True:
    im = picam2.capture_array()

    cv2.imshow("image",im)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
time.sleep(0)

