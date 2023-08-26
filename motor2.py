import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(28, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(30, GPIO.OUT)

# Define the sequence of steps
seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]

# Define the number of steps per revolution
steps_per_rev = 512

# Define the speed (in revolutions per minute)
rpm = 5

# Calculate the delay between steps (in seconds)
delay = 60 / (steps_per_rev * rpm)

# Run the motor
for i in range(steps_per_rev):
    for halfstep in range(8):
        for pin in range(4):
            GPIO.output(27+pin, seq[halfstep][pin])
        time.sleep(delay)
