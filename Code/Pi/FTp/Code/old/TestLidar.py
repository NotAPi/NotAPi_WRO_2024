import time
import pigpio
import os
import sys

try:
    os.system("sudo pigpiod")  # Launching GPIO library
    time.sleep(1)  # As it takes some time to launch
except:
    print("GPIO library already launched")
    pass

# 55------105---155

# Initialize pigpio
pi = pigpio.pi()

L_RX_PIN = 22
R_RX_PIN = 24
F_RX_PIN = 25

IN1_PIN = 10
IN2_PIN = 11
ENA_PIN = 12

SERVO_PIN = 17


Laps = 0
# Try to close the serial connection if it is already open
try:
    pi.bb_serial_read_close(R_RX_PIN)
    pi.bb_serial_read_close(L_RX_PIN)
    pi.bb_serial_read_close(F_RX_PIN)
except:
    pass



# Set up the software serial connection
pi.set_mode(R_RX_PIN, pigpio.INPUT)
pi.bb_serial_read_open(R_RX_PIN, 115200)
pi.set_mode(L_RX_PIN, pigpio.INPUT)
pi.bb_serial_read_open(L_RX_PIN, 115200)
pi.set_mode(F_RX_PIN, pigpio.INPUT)
pi.bb_serial_read_open(F_RX_PIN, 115200)
print("init done")

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
        if distance is not None: # Isn't really needed
            # print(f"DistanceR: {distance} cm, Strength: {strength}")
            return distance

def R_read_lidar():
    while True:
        (count, data) = pi.bb_serial_read(R_RX_PIN)
        if count > 0:
            break
    if count > 0:
        distance, strength = parse_lidar_data(data)
        if distance is not None: # Isn't really needed
            # print(f"DistanceR: {distance} cm, Strength: {strength}")
            return distance

def L_read_lidar():
    while True:
        (count, data) = pi.bb_serial_read(L_RX_PIN)
        if count > 0:
            break
    if count > 0:
        distance, strength = parse_lidar_data(data)
        if distance is not None: # Isn't really needed
            # print(f"DistanceL: {distance} cm, Strength: {strength}")
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
    time.sleep(0.25)
    if angle == 90:
        servo(155)
        forward(255)
        time.sleep(2)

def turnLeft(angle=90):
    stop()
    time.sleep(0.25)
    if angle == 90:
        servo(55)
        forward(255)
        time.sleep(2)

def forwardm(distance=1):
    forward(255)
    time.sleep(6.6*distance)

try:
    servo(105)
    forward()
    time.sleep(1)
    while Laps < 3:
        
        LastClose = 0
        # Get Front distance    
        Fdistance = F_read_lidar()
        # print("F:")
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
        # print("L:")
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
        # print("R:")
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
        
        
        # print(Fdistance)
        print("CheckFront")
        time.sleep(0.1)
        if Fdistance < 15:
            if LastClose == 0:
                LastClose == 1
                print("close")
            elif LastClose == 1:
                print("stop") 
                stop()
            else:
                print("??? Front")
        else:
            LastClose = 0
            print("good")
            forward()

            # forward()
            # Ldistance = L_read_lidar()
            # Rdistance = R_read_lidar()
            
            # while Ldistance is None:
            #     Ldistance = L_read_lidar()
            
            # while Rdistance is None:
            #     Rdistance = R_read_lidar()
            
            print(time.strftime("%Y-%m-%d %H:%M:%S") + " F: " + str(Fdistance) + " L: " + str(Ldistance) + " R: " + str(Rdistance))

            if Ldistance > 150:
                print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
                servo(55) 
                forward()
                time.sleep(2)
                servo()
                time.sleep(2)
                stop()
                time.sleep(2)
            
            
            if Rdistance > 150: 
                print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
                servo(155)
                forward()
                time.sleep(2)
                servo()
                time.sleep(2)
                stop()
                time.sleep(2)
           
            if Ldistance > Rdistance * 0.9:
                servo(55)  # Turn left
                print("55")
            elif Rdistance > Ldistance * 0.9:
                servo(155)  # Turn right
                print("155")
            else:
                servo(105)  # Go straight
                print("105")
                    
        time.sleep(0.1)
        
        
        # forward()

        # angle = int(input("angle: "))
        # servo(angle)
        

except KeyboardInterrupt:
    stop()
    pi.bb_serial_read_close(R_RX_PIN)  # Close the serial connection on exit
    pi.bb_serial_read_close(L_RX_PIN)  # Close the serial connection on exit
    pi.bb_serial_read_close(F_RX_PIN)  # Close the serial connection on exit

    pi.stop()