# OpenCV list all video devices attached to the computer
import cv2
import numpy as np
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

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
        height, width, _ = 480, 639, 3
        third_width = width // 3
        frame.resize((height, width, 3))

        # Split the screen into three parts
        left_part = frame[:, :third_width]
        middle_part = frame[:, third_width:2*third_width]
        right_part = frame[:, 2*third_width:]

        # Filter out red and green for each part
        left_red_mask = left_part[:, :, 2] > 1.5 * left_part[:, :, 1]
        left_green_mask = left_part[:, :, 1] > 1.5 * left_part[:, :, 2]
        left_color = "Green" if np.sum(left_green_mask) > np.sum(left_red_mask) else "Red"

        middle_red_mask = middle_part[:, :, 2] > 1.5 * middle_part[:, :, 1]
        middle_green_mask = middle_part[:, :, 1] > 1.5 * middle_part[:, :, 2]
        middle_color = "Green" if np.sum(middle_green_mask) > np.sum(middle_red_mask) else "Red"

        right_red_mask = right_part[:, :, 2] > 1.5 * right_part[:, :, 1]
        right_green_mask = right_part[:, :, 1] > 1.5 * right_part[:, :, 2]
        right_color = "Green" if np.sum(right_green_mask) > np.sum(right_red_mask) else "Red"

        # print(f"{left_color} {middle_color} {right_color}")
        # print(type(left_red_mask))
        left_red = cv2.bitwise_and(left_part, left_part, mask=left_red_mask.astype(np.uint8))
        left_green = cv2.bitwise_and(left_part, left_part, mask=left_green_mask.astype(np.uint8))

        middle_red = cv2.bitwise_and(middle_part, middle_part, mask=middle_red_mask.astype(np.uint8))
        middle_green = cv2.bitwise_and(middle_part, middle_part, mask=middle_green_mask.astype(np.uint8))

        right_red = cv2.bitwise_and(right_part, right_part, mask=right_red_mask.astype(np.uint8))
        right_green = cv2.bitwise_and(right_part, right_part, mask=right_green_mask.astype(np.uint8))

        # Combine the red and green parts
        left_combined = cv2.addWeighted(left_red, 0.5, left_green, 0.5, 0)
        middle_combined = cv2.addWeighted(middle_red, 0.5, middle_green, 0.5, 0)
        right_combined = cv2.addWeighted(right_red, 0.5, right_green, 0.5, 0)

        # Combine the three parts back into a single image
        combined = np.hstack((left_combined, middle_combined, right_combined))

        # Display the image using matplotlib
        # plt.imshow(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB))
        # plt.pause(0.001)  # Pause to update the plot
        # plt.draw()
        print((width, height))
        left_red_mask = cv2.resize(left_red_mask.astype(np.uint8), (width, height))
        left_green_mask = cv2.resize(left_green_mask.astype(np.uint8), (width, height))

        frame_red = cv2.bitwise_and(frame, frame, mask=left_red_mask.astype(np.uint8))
        frame_green = cv2.bitwise_and(frame, frame, mask=left_green_mask.astype(np.uint8))
        # Combine the red and green parts
        frame_combined = cv2.addWeighted(frame_red, 0.5, frame_green, 0.5, 0)
        # Display the combined image using matplotlib
        plt.imshow(cv2.cvtColor(frame_combined, cv2.COLOR_BGR2RGB))
        plt.pause(0.001)  # Pause to update the plot
        plt.draw()
        # Apply red and green masks on the original image




        # cv2.imwrite("screenshot.jpg", frame)
        time.sleep(.1)
        # print green or red, whats more on the image
        # print("Green" if np.sum(green_mask) > np.sum(red_mask) else "Red")
        
cap.release()

