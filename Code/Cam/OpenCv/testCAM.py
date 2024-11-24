from picamera2 import Picamera2
import cv2
import time

# Initialize the Raspberry Pi camera
picam2 = Picamera2()
# Configure the camera without specifying a resolution to use the default resolution
picam2.configure(picam2.create_preview_configuration())
picam2.start()

# Allow the camera to warm up
time.sleep(0.1)

# Capture an image
image = picam2.capture_array()

# Display the image using OpenCV
cv2.imshow("Captured Image", image)
cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()
