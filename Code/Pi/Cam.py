# OpenCV list all video devices attached to the computer
import cv2
import numpy as np
import time

def find_camera():
    for i in range(0, 10):
        cap = cv2.VideoCapture(i)
        test, frame = cap.read()
        if test:
            cap.release()
            return i
        cap.release()
    return None

camera_number = find_camera()
print(f"Camera found: {camera_number}" if camera_number is not None else "No camera found")

# Take a screenshot and save it to a file named "screenshot.jpg" (temp)
cap = cv2.VideoCapture(camera_number)
while True:
    ret, frame = cap.read()
    if ret:
        # Filter out red and green
        red_mask = frame[:, :, 2] > 1.5 * frame[:, :, 1]
        green_mask = frame[:, :, 1] > 1.5 * frame[:, :, 2]
        frame[red_mask] = [0, 0, 255]  # Set red pixels to red (BGR format)
        frame[green_mask] = [0, 255, 0]  # Set green pixels to green (BGR format)
        frame[~(red_mask | green_mask)] = [0, 0, 0]  # Set non-red and non-green pixels to black (BGR format)

        cv2.imwrite("screenshot.jpg", frame)
        time.sleep(.1)
        print("Green" if np.sum(green_mask) > np.sum(red_mask) else "Red")

cap.release()
