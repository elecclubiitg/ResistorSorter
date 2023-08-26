from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time
import math
from resistor_detectection_s import isResistor

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

while True:
    frame = picam2.capture_array()
    isResistor(frame)