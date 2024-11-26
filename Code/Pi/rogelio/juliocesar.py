import cv2
import numpy as np
from picamera2 import Picamera2
import time
import pigpio
import os

# Initialize the camera and pigpio
os.system("sudo pigpiod")
time.sleep(1)
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()
time.sleep(0.1)

# Initialize pigpio
pi = pigpio.pi()

# Define GPIO pins
IN1_PIN = 10
IN2_PIN = 11
ENA_PIN = 12

def forward(speed=255):
    pi.write(IN1_PIN, 0)
    pi.write(IN2_PIN, 1)
    pi.set_PWM_dutycycle(ENA_PIN, speed)

def correct_direction_based_on_color():
    while True:
        # Capture image
        image = picam2.capture_array()
        
        # Convert image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define color range for detection (example: red color)
        lower_color = np.array([0, 120, 70])
        upper_color = np.array([10, 255, 255])
        
        # Create a mask for the color
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Calculate the center of the contour
            center_x = x + w // 2
            
            # Get image dimensions
            altura, anchura = image.shape[:2]
            image_center_x = anchura // 2
            
            # Correct direction based on the position of the color
            if center_x < image_center_x - 20:
                # Turn left
                pi.write(IN1_PIN, 1)
                pi.write(IN2_PIN, 0)
            elif center_x > image_center_x + 20:
                # Turn right
                pi.write(IN1_PIN, 0)
                pi.write(IN2_PIN, 1)
            else:
                # Move forward
                forward()
        
        # Display the result
        cv2.imshow("Frame", image)
        cv2.waitKey(1)

# Run the correction function
correct_direction_based_on_color()