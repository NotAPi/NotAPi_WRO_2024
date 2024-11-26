import time
import pigpio
import atexit

# Initialize pigpio
pi = pigpio.pi()

def close_gpio():
    if pi is not None:
        try:
            pi.bb_serial_read_close(R_RX_PIN)
            pi.bb_serial_read_close(L_RX_PIN)
            pi.bb_serial_read_close(F_RX_PIN)
        except pigpio.error as e:
            print(f"Error closing GPIO: {e}")
        pi.stop()

atexit.register(close_gpio)

# Define pins
L_RX_PIN = 22
R_RX_PIN = 24
F_RX_PIN = 25

# Ensure GPIO pins are not in use before opening them
try:
    pi.bb_serial_read_close(L_RX_PIN)
    pi.bb_serial_read_close(R_RX_PIN)
    pi.bb_serial_read_close(F_RX_PIN)
except pigpio.error:
    pass

# Set up the software serial connection
pi.set_mode(L_RX_PIN, pigpio.INPUT)
pi.bb_serial_read_open(L_RX_PIN, 115200)
pi.set_mode(R_RX_PIN, pigpio.INPUT)
pi.bb_serial_read_open(R_RX_PIN, 115200)
pi.set_mode(F_RX_PIN, pigpio.INPUT)
pi.bb_serial_read_open(F_RX_PIN, 115200)

# Function to parse lidar data
def parse_lidar_data(data):
    if len(data) >= 9 and data[0] == 0x59 and data[1] == 0x59:
        distance = data[2] + data[3] * 256
        strength = data[4] + data[5] * 256
        return distance, strength
    return None, None

def L_read_lidar():
    while True:
        (count, data) = pi.bb_serial_read(L_RX_PIN)
        if count > 0:
            distance, strength = parse_lidar_data(data)
            if distance is not None:
                return distance

def R_read_lidar():
    while True:
        (count, data) = pi.bb_serial_read(R_RX_PIN)
        if count > 0:
            distance, strength = parse_lidar_data(data)
            if distance is not None:
                return distance

def F_read_lidar():
    while True:
        (count, data) = pi.bb_serial_read(F_RX_PIN)
        if count > 0:
            distance, strength = parse_lidar_data(data)
            if distance is not None:
                return distance

def L_Loop():
    while True:
        LdistanceTemp1 = L_read_lidar()
        LdistanceTemp2 = L_read_lidar()

        while (LdistanceTemp1 is None or 0 < LdistanceTemp1 > 500) or (LdistanceTemp2 is None or 0 < LdistanceTemp2 > 500):
            if LdistanceTemp1 is None or 0 < LdistanceTemp1 > 500:
                LdistanceTemp1 = L_read_lidar()
            if LdistanceTemp2 is None or 0 < LdistanceTemp2 > 500:
                LdistanceTemp2 = L_read_lidar()
            print(f"L Invalid readings: {LdistanceTemp1}, {LdistanceTemp2}")

        return min(LdistanceTemp1, LdistanceTemp2)

def R_Loop():
    while True:
        RdistanceTemp1 = R_read_lidar()
        RdistanceTemp2 = R_read_lidar()

        while (RdistanceTemp1 is None or 0 < RdistanceTemp1 > 500) or (RdistanceTemp2 is None or 0 < RdistanceTemp2 > 500):
            if RdistanceTemp1 is None or 0 < RdistanceTemp1 > 500:
                RdistanceTemp1 = R_read_lidar()
            if RdistanceTemp2 is None or 0 < RdistanceTemp2 > 500:
                RdistanceTemp2 = R_read_lidar()
            print(f"R Invalid readings: {RdistanceTemp1}, {RdistanceTemp2}")

        return min(RdistanceTemp1, RdistanceTemp2)

def F_Loop():
    while True:
        FdistanceTemp1 = F_read_lidar()
        FdistanceTemp2 = F_read_lidar()

        while (FdistanceTemp1 is None or 0 < FdistanceTemp1 > 500) or (FdistanceTemp2 is None or 0 < FdistanceTemp2 > 500):
            if FdistanceTemp1 is None or 0 < FdistanceTemp1 > 500:
                FdistanceTemp1 = F_read_lidar()
            if FdistanceTemp2 is None or 0 < FdistanceTemp2 > 500:
                FdistanceTemp2 = F_read_lidar()
            print(f"F Invalid readings: {FdistanceTemp1}, {FdistanceTemp2}")

        return min(FdistanceTemp1, FdistanceTemp2)

def distance_loop():
    while True:
        Ldistance, Rdistance, Fdistance = L_Loop(), R_Loop(), F_Loop()
        print("L " + str(Ldistance) + " R " + str(Rdistance) + " F " + str(Fdistance))
        time.sleep(0.2)

if __name__ == "__main__":
    try:
        distance_loop()
    except KeyboardInterrupt:
        close_gpio()