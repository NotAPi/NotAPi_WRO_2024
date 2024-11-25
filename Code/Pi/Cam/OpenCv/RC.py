import time
import pigpio
import os
from pynput import keyboard
import cv2
from picamera2 import Picamera2

try:
    os.system("sudo pigpiod")  # Launching GPIO library
    time.sleep(1)  # As it takes some time to launch
except:
    pass

# Initialize pigpio
pi = pigpio.pi()

# Define pins
IN1_PIN = 10
IN2_PIN = 11
ENA_PIN = 12
SERVO_PIN = 17

def forward(speed=255):
    pi.write(IN1_PIN, 0)
    pi.write(IN2_PIN, 1)
    pi.set_PWM_dutycycle(ENA_PIN, speed)

def stop():
    pi.write(IN1_PIN, 0)
    pi.write(IN2_PIN, 0)
    pi.set_PWM_dutycycle(ENA_PIN, 0)

def servo(angle=105):
    pulse_width = 500 + (angle / 180.0) * 2000
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

# Define the key press actions
def on_press_key(key):
    try:
        if key.char == 'w':
            forward()
        elif key.char == 's':
            stop()
        elif key.char == 'a':
            servo(55)
        elif key.char == 'd':
            servo(155)
        elif key.char == 'x':
            stop()  # Example for stopping
        elif key.char == 'e':
            servo(105)
    except AttributeError:
        pass

# Start the keyboard listener
listener = keyboard.Listener(on_press=on_press_key)
listener.start()

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

try:
    while True:
        # Capture image
        image = picam2.capture_array()

        # Display the image
        cv2.imshow('original', image)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Keep the script running to listen for key presses
        time.sleep(0.1)
except KeyboardInterrupt:
    stop()
    pi.stop()
finally:
    cv2.destroyAllWindows()