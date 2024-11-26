import pigpio
import time

# Initialize pigpio
pi = pigpio.pi()

# Define the pin for the LIDAR sensor
LIDAR_PIN = 22

# Set up the software serial connection
pi.set_mode(LIDAR_PIN, pigpio.INPUT)
pi.bb_serial_read_open(LIDAR_PIN, 115200)

# Function to parse lidar data
def parse_lidar_data(data):
    if len(data) >= 9 and data[0] == 0x59 and data[1] == 0x59:
        distance = data[2] + data[3] * 256
        strength = data[4] + data[5] * 256
        return distance, strength
    return None, None

# Function to read lidar data
def read_lidar():
    while True:
        (count, data) = pi.bb_serial_read(LIDAR_PIN)
        if count > 0:
            distance, strength = parse_lidar_data(data)
            if distance is not None:
                return distance

# Read and print the LIDAR distance
try:
    while True:
        distance = read_lidar()
        print(f"Distance: {distance}")
        time.sleep(0.2)
except KeyboardInterrupt:
    pi.bb_serial_read_close(LIDAR_PIN)
    pi.stop()