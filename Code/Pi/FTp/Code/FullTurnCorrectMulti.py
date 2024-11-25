import time
import pigpio
import os
import sys
import threading

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

Ldistance = 0
Rdistance = 0
Fdistance = 0

lock = threading.Lock()


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
    
def distance_loop():
    global Ldistance, Rdistance, Fdistance
    while True:
        Ldistance, Rdistance, Fdistance = distances()
        print("L " + str(Ldistance) + " R " + str(Rdistance) + " F " + str(Fdistance))
        time.sleep(0.2)

def F_Loop():
    global Fdistance
    while True:
        with lock:
            FdistanceTemp1 = F_read_lidar()
            time.sleep(0.05)  # Short delay before the second reading
            FdistanceTemp2 = F_read_lidar()
            
            if FdistanceTemp1 is not None and FdistanceTemp2 is not None and FdistanceTemp1 < 500 and FdistanceTemp2 < 500:
                # Check if the two readings are within 25% of each other
                lower_bound = FdistanceTemp1 * 0.75
                upper_bound = FdistanceTemp1 * 1.25
                if lower_bound <= FdistanceTemp2 <= upper_bound:
                    Fdistance = FdistanceTemp2
                    print(f"Fdistance updated: {Fdistance}")
                else:
                    print(f"Fdistance not updated: {FdistanceTemp1} and {FdistanceTemp2} are not within 25% of each other")
            else:
                print(f"Invalid readings: {FdistanceTemp1}, {FdistanceTemp2}")
            
            time.sleep(0.1)

def L_Loop():
    global Ldistance
    while True:
        with lock:
            LdistanceTemp1 = L_read_lidar()
            time.sleep(0.05)  # Short delay before the second reading
            LdistanceTemp2 = L_read_lidar()
            
            if LdistanceTemp1 is not None and LdistanceTemp2 is not None and LdistanceTemp1 < 500 and LdistanceTemp2 < 500:
                # Check if the two readings are within 25% of each other
                lower_bound = LdistanceTemp1 * 0.75
                upper_bound = LdistanceTemp1 * 1.25
                if lower_bound <= LdistanceTemp2 <= upper_bound:
                    Ldistance = LdistanceTemp2
                    print(f"Ldistance updated: {Ldistance}")
                else:
                    print(f"Ldistance not updated: {LdistanceTemp1} and {LdistanceTemp2} are not within 25% of each other")
            else:
                print(f"Invalid readings: {LdistanceTemp1}, {LdistanceTemp2}")
            
            time.sleep(0.1)

def R_Loop():
    global Rdistance
    while True:
        with lock:
            RdistanceTemp1 = R_read_lidar()
            time.sleep(0.05)  # Short delay before the second reading
            RdistanceTemp2 = R_read_lidar()
            
            if RdistanceTemp1 is not None and RdistanceTemp2 is not None and RdistanceTemp1 < 500 and RdistanceTemp2 < 500:
                # Check if the two readings are within 25% of each other
                lower_bound = RdistanceTemp1 * 0.75
                upper_bound = RdistanceTemp1 * 1.25
                if lower_bound <= RdistanceTemp2 <= upper_bound:
                    Rdistance = RdistanceTemp2
                    print(f"Rdistance updated: {Rdistance}")
                else:
                    print(f"Rdistance not updated: {RdistanceTemp1} and {RdistanceTemp2} are not within 25% of each other")
            else:
                print(f"Invalid readings: {RdistanceTemp1}, {RdistanceTemp2}")
            
            time.sleep(0.1)

# def R_Loop():
#     global Rdistance
#     while True:
#         with lock:
#             RdistanceTemp = R_read_lidar()
#             if RdistanceTemp is not None and RdistanceTemp < 500:
#                 Rdistance = RdistanceTemp
#                 print(f"Rdistance updated: {Rdistance}")

#             time.sleep(0.1)

def distances():
    global Ldistance, Rdistance, Fdistance
    # Get Front distance    
    #aaaprint("F")
    FdistanceTemp = F_read_lidar()
    # #aaaprint("F:")
    if Fdistance is not None:
        Fdistance = FdistanceTemp               
    else:
        while True:
            Fdistance = F_read_lidar()
            if Fdistance is not None:
                break
    #aaaprint("F done")
    
    #aaaprint("L")
    
    # Get Left distance    
    Ldistance = L_read_lidar()
    # #aaaprint("L:")
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
    #aaaprint("L done")
    
    #aaaprint("R")
    # Get Right distance    
    Rdistance = R_read_lidar()
    # #aaaprint("R:")
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
    #aaaprint("R done")
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

def main():
    global Ldistance, Rdistance, Fdistance
    try:
        servo()
        time.sleep(0.05)
        forward()
        giros = 0
        while True:
            while Ldistance < 100 or Rdistance < 100:
                forward()
                # Ldistance, Rdistance, Fdistance = distances()
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
            # Ldistance, Rdistance, Fdistance = distances()

            while int(Fdistance) > 165:
                forward()
                # Ldistance, Rdistance, Fdistance = distances()
                print("L " + str(Ldistance) + " R " + str(Rdistance) + " SUM " + str(Ldistance + Rdistance) + " F " + str(Fdistance))
                time.sleep(0.2)
                #aaaprint ("F " + str(Fdistance))
                if int(Fdistance) < 165:
                    break
            
            if giros == 12:
                break
            #aaaprint("150")
            
            #aaaprint("Correct time")
            # Ldistance, Rdistance, Fdistance = distances()
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
        
if __name__ == "__main__":
    try:
            
        R_loop_thread = threading.Thread(target=R_Loop)
        L_loop_thread = threading.Thread(target=L_Loop)
        F_loop_thread = threading.Thread(target=F_Loop)
        main_thread = threading.Thread(target=main)
        
        R_loop_thread.start()
        L_loop_thread.start()
        F_loop_thread.start()
        main_thread.start()
        
        R_loop_thread.join()
        L_loop_thread.join()
        F_loop_thread.join()
        main_thread.join()
    except KeyboardInterrupt:
        stop()
        pi.bb_serial_read_close(R_RX_PIN)  # Close the serial connection on exit
        pi.bb_serial_read_close(L_RX_PIN)  # Close the serial connection on exit
        pi.bb_serial_read_close(F_RX_PIN)  # Close the serial connection on exit

        pi.stop()    
    
    