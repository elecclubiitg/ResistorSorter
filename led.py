import RPi.GPIO as GP
import time

Led_pin = 17

GP.setmode(GP.BCM)
GP.setup(Led_pin, GP.OUT)

GP.output(Led_pin,GP.HIGH)
#time.sleep(10)


