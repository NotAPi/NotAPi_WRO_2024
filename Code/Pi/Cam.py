# OpenCV list all video devices attached to the computer
import cv2

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

# Video device = 0. Take a screenshot and save it to a file named "screenshot.jpg"
cap = cv2.VideoCapture(camera_number)
ret, frame = cap.read()
cv2.imwrite("screenshot.jpg", frame)
cap.release()
