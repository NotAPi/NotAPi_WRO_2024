import time
import pigpio
import os
from pynput import keyboard
import cv2
from picamera2 import Picamera2
import time
import pigpio

try:

    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    picam2.start()

    image = picam2.capture_array()

    cv2.imshow('original', image)

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
                backward()  # Example for turning servo left
            elif key.char == 'e':
                servo(105)
        except AttributeError:
            pass

    # Start the keyboard listener
    listener = keyboard.Listener(on_press=on_press_key)
    listener.start()


    try:
        os.system("sudo pigpiod")  # Launching GPIO library
        time.sleep(1)  # As it takes some time to launch
    except:
        pass

    # Initialize pigpio
    pi = pigpio.pi()

    # Define pins
    L_RX_PIN = 22
    R_RX_PIN = 24
    F_RX_PIN = 25
    IN1_PIN = 10
    IN2_PIN = 11
    ENA_PIN = 12
    SERVO_PIN = 17

    # Set up the software serial connection
    pi.set_mode(R_RX_PIN, pigpio.INPUT)
    pi.bb_serial_read_open(R_RX_PIN, 115200)
    pi.set_mode(L_RX_PIN, pigpio.INPUT)
    pi.bb_serial_read_open(L_RX_PIN, 115200)
    pi.set_mode(F_RX_PIN, pigpio.INPUT)
    pi.bb_serial_read_open(F_RX_PIN, 115200)

    def parse_lidar_data(data):
        if len(data) >= 9 and data[0] == 0x59 and data[1] == 0x59:
            distance = data[2] + data[3] * 256
            strength = data[4] + data[5] * 256
            return distance, strength
        return None, None

    def F_read_lidar():
        while True:
            (count, data) = pi.bb_serial_read(F_RX_PIN)
            if count > 0:
                break
        if count > 0:
            distance, strength = parse_lidar_data(data)
            if distance is not None:
                return distance

    def R_read_lidar():
        while True:
            (count, data) = pi.bb_serial_read(R_RX_PIN)
            if count > 0:
                break
        if count > 0:
            distance, strength = parse_lidar_data(data)
            if distance is not None:
                return distance

    def L_read_lidar():
        while True:
            (count, data) = pi.bb_serial_read(L_RX_PIN)
            if count > 0:
                break
        if count > 0:
            distance, strength = parse_lidar_data(data)
            if distance is not None:
                return distance



    def forward(speed=255):
        pi.write(IN1_PIN, 0)
        pi.write(IN2_PIN, 1)
        pi.set_PWM_dutycycle(ENA_PIN, speed)

    def backward(speed=255):
        pi.write(IN1_PIN, 1)
        pi.write(IN2_PIN, 0)
        pi.set_PWM_dutycycle(ENA_PIN, speed)

    def stop():
        pi.write(IN1_PIN, 0)
        pi.write(IN2_PIN, 0)
        pi.set_PWM_dutycycle(ENA_PIN, 0)

    def servo(angle=105):
        pulse_width = 500 + (angle / 180.0) * 2000
        pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

    def turnRight(angle=90):
        stop()
        time.sleep(0.05)
        if angle == 90:
            servo(155)
            forward(255)
            time.sleep(1.95)

    def turnLeft(angle=90):
        stop()
        time.sleep(0.05)
        if angle == 90:
            servo(55)
            forward(255)
            time.sleep(1.95)

    def forwardm(distance=1):
        forward(255)
        time.sleep(6.6*distance)

    def distances():
        Fdistance = F_read_lidar()
        if Fdistance is None:
            try: 
                Fdistance = FdistanceOld
            except:
                while True:
                    Fdistance = F_read_lidar()
                    if Fdistance is not None:
                        break                
        else:
            FdistanceOld = Fdistance

        # Get Left distance    
        Ldistance = L_read_lidar()
        if Ldistance is None:
            try: 
                Ldistance = LdistanceOld
            except:
                while True:
                    Ldistance = L_read_lidar()
                    if Ldistance is not None:
                        break                
        else:
            LdistanceOld = Ldistance

        # Get Right distance    
        Rdistance = R_read_lidar()
        if Rdistance is None:
            try: 
                Rdistance = RdistanceOld
            except:
                while True:
                    Rdistance = R_read_lidar()
                    if Rdistance is not None:
                        break                
        else:
            RdistanceOld = Rdistance

        return Ldistance, Rdistance, Fdistance

    def turnLeftFull():
        servo()
        forwardm(0.2)
        turnLeft(90)
        
        servo()
        stop()
        time.sleep(0.05)
        forward()
        time.sleep(0.1)
        Ldistance, Rdistance, Fdistance = distances()
        stop()

        while Ldistance + Rdistance > 150:
            forward()
            Ldistance, Rdistance, Fdistance = distances()
            time.sleep(0.2)
        time.sleep(0.05)    
        stop()
        
    def turnRightFull():
        servo(105)
        forwardm(0.2)
        turnRight(90)
        
        servo()
        stop()
        time.sleep(0.05)
        forward()
        time.sleep(0.1)
        Ldistance, Rdistance, Fdistance = distances()
        stop()

        while Ldistance + Rdistance > 150:
            forward()
            Ldistance, Rdistance, Fdistance = distances()
            time.sleep(0.2)
        time.sleep(0.05)    
        stop()



    # Register the key press events
    listener = keyboard.Listener(on_press=on_press_key)
    listener.start()

    try:
        while True:
            # Keep the script running to listen for key presses
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop()
        pi.stop()

except:
    stop()
    pi.stop()