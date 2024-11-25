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

# Capture and display video frames
while True:
    # Capture a frame
    image = picam2.capture_array()

    # Swap the red and blue channels
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Display the frame using OpenCV
    cv2.imshow("Video Stream", image_rgb)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
picam2.stop()
