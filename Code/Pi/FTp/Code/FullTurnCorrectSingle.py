import time
import pigpio
import os
import sys

try:
    os.system("sudo pigpiod")  # Launching GPIO library
    time.sleep(1)  # As it takes some time to launch
except:
    #aaaprint("GPIO library already launched")
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
#aaaprint("init done")

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
            # #aaaprint(f"DistanceR: {distance} cm, Strength: {strength}")
            return distance

def R_read_lidar():
    while True:
        (count, data) = pi.bb_serial_read(R_RX_PIN)
        if count > 0:
            break
    if count > 0:
        distance, strength = parse_lidar_data(data)
        if distance is not None: # Isn't really needed
            # #aaaprint(f"DistanceR: {distance} cm, Strength: {strength}")
            return distance

def L_read_lidar():
    while True:
        (count, data) = pi.bb_serial_read(L_RX_PIN)
        if count > 0:
            break
    if count > 0:
        distance, strength = parse_lidar_data(data)
        if distance is not None: # Isn't really needed
            # #aaaprint(f"DistanceL: {distance} cm, Strength: {strength}")
            return distance
        
        
        
def F_Read():
    global Fdistance
    FdistanceTemp1 = F_read_lidar()
    if FdistanceTemp1 is not None and FdistanceTemp1 < 500:
            Fdistance = FdistanceTemp1
            return Fdistance
            print(f"Fdistance updated: {Fdistance}")
    else:
        print(f"F Invalid readings: {FdistanceTemp1}")
    
    time.sleep(0.1)

def L_Read():
    global Ldistance
    LdistanceTemp1 = L_read_lidar()
    if LdistanceTemp1 is not None and LdistanceTemp1 < 500:
            Ldistance = LdistanceTemp1
            return Ldistance
            print(f"Ldistance updated: {Ldistance}")
    else:
        print(f"L Invalid readings: {LdistanceTemp1}")
    
    time.sleep(0.1)

def R_Read():
    global Rdistance
    RdistanceTemp1 = R_read_lidar()
    if RdistanceTemp1 is not None and RdistanceTemp1 < 500:
            Rdistance = RdistanceTemp1
            return Rdistance
            print(f"Rdistance updated: {Rdistance}")
    else:
        print(f"R Invalid readings: {RdistanceTemp1}")
    
    time.sleep(0.1)

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
    
    # Get Front distance    
    #aaaprint("F")
    Fdistance = F_Read()
    # #aaaprint("F:")
    #aaaprint("L")
    
    # Get Left distance    
    Ldistance = L_Read()
    # #aaapr
    Rdistance = R_Read()
    
    #aaaprint("return")
    return Ldistance, Rdistance, Fdistance

def turnLeftFull():
    servo(105)
    forwardm(0.2)
    turnLeft(90)
    
    servo()
    # forwardm(0.5)

    stop()
    time.sleep(0.05)
    #aaaprint("read")
    forward()
    time.sleep(0.1)
    Ldistance, Rdistance, Fdistance = distances()
    #aaaprint("read done")
    stop()
    #aaaprint("L " + str(Ldistance) + " R " + str(Rdistance) + " SUM " + str(Ldistance + Rdistance) + " F " + str(Fdistance))

    while Ldistance + Rdistance > 150:
        forward()
        Ldistance, Rdistance, Fdistance = distances()
        #aaaprint("L " + str(Ldistance) + " R " + str(Rdistance) + " SUM " + str(Ldistance + Rdistance) + " F " + str(Fdistance))
        # forward()        
        time.sleep(0.2)
    #aaaprint("Stop")
    time.sleep(0.05)    
    stop()
    
def turnRightFull():
    servo(105)
    forwardm(0.2)
    turnRight(90)
    
    servo()
    # forwardm(0.5)

    stop()
    time.sleep(0.05)
    #aaaprint("read")
    forward()
    time.sleep(0.1)
    Ldistance, Rdistance, Fdistance = distances()
    #aaaprint("read done")
    stop()
    #aaaprint("L " + str(Ldistance) + " R " + str(Rdistance) + " SUM " + str(Ldistance + Rdistance) + " F " + str(Fdistance))

    while Ldistance + Rdistance > 150:
        forward()
        Ldistance, Rdistance, Fdistance = distances()
        #aaaprint("L " + str(Ldistance) + " R " + str(Rdistance) + " SUM " + str(Ldistance + Rdistance) + " F " + str(Fdistance))
        # forward()        
        time.sleep(0.2)
    #aaaprint("Stop")
    time.sleep(0.05)    
    stop()
    
try:
    servo()
    time.sleep(0.05)
    forward()
    giros = 0
    while True:
        Ldistance, Rdistance, Fdistance = distances()
        while Ldistance < 100 or Rdistance < 100:
            forward()
            Ldistance, Rdistance, Fdistance = distances()
            print("L " + str(Ldistance) + " R " + str(Rdistance) + " SUM " + str(Ldistance + Rdistance) + " F " + str(Fdistance))
            time.sleep(0.2)
            if Ldistance + Rdistance > 110:
                break
        #aaaprint("Turn time")
        
        if Ldistance > Rdistance:
            turnLeftFull()
            giros = giros + 1
            #aaaprint("Left")
        
        if Rdistance > Ldistance:
            turnRightFull()
            giros = giros + 1
            #aaaprint("Right")
        forward()
        Ldistance, Rdistance, Fdistance = distances()

        while int(Fdistance) > 165:
            forward()
            Ldistance, Rdistance, Fdistance = distances()
            print("L " + str(Ldistance) + " R " + str(Rdistance) + " SUM " + str(Ldistance + Rdistance) + " F " + str(Fdistance))
            time.sleep(0.2)
            #aaaprint ("F " + str(Fdistance))
            if int(Fdistance) < 165:
                break
        
        if giros == 12:
            break
        #aaaprint("150")
        
        #aaaprint("Correct time")
        Ldistance, Rdistance, Fdistance = distances()
        #aaaprint("L " + str(Ldistance) + " R " + str(Rdistance) + " SUM " + str(Ldistance + Rdistance) + " F " + str(Fdistance))
        stop()
        
        if Ldistance > Rdistance * 0.9:
            servo(95)  # Turn left
            #aaaprint("90")
        elif Rdistance > Ldistance * 0.9:
            servo(115)  # Turn right
            #aaaprint("120")
        else:
            servo(105)  # Go straight
            #aaaprint("105")
        forwardm(0.1)
        servo()
    
        for a in range(5):
            print(giros)
        
    stop()

        
        

except KeyboardInterrupt:
    stop()
    pi.bb_serial_read_close(R_RX_PIN)  # Close the serial connection on exit
    pi.bb_serial_read_close(L_RX_PIN)  # Close the serial connection on exit
    pi.bb_serial_read_close(F_RX_PIN)  # Close the serial connection on exit

    pi.stop()