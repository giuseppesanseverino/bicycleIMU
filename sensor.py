import time
import math
from multiprocessing.connection import Connection
import board
import busio

from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from bicycleinit.BicycleSensor import BicycleSensor

def main(bicycleinit: Connection, name: str, args: dict):
    sensor = BicycleSensor(bicycleinit, name, args)
    
    # Initialize I2C and IMU
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        imu = LSM6DSOX(i2c)
    except Exception as e:
        sensor.send_msg({'type': 'log', 'level': 'error', 'msg': f"Failed to init IMU over I2C: {e}"})
        sensor.shutdown()
        return

    # Write the CSV header
    sensor.write_header(['acc_x', 'acc_y', 'acc_z', 'pitch', 'roll'])
    
    RAD_TO_DEG = 180.0 / math.pi
    
    sensor.send_msg("Started IMU Data Collection (LSM6DSO32)")

    try:
        while True:
            # Read Acceleration
            acc_x, acc_y, acc_z = imu.acceleration

            acc_x_f, acc_y_f, acc_z_f = float(accel_x), float(accel_y), float(accel_z)

            # Calculate Pitch and Roll
            pitch_rad = math.atan2(-acc_x_f, math.sqrt(acc_y_f**2 + acc_z_f**2))
            pitch = pitch_rad * RAD_TO_DEG
            
            roll_rad = math.atan2(acc_y_f, acc_z_f)
            roll = roll_rad * RAD_TO_DEG
            
            # Send Data to logger (at roughly 20Hz)
            sensor.write_measurement([acc_x_f, acc_y_f, acc_z_f, pitch, roll])
            time.sleep(0.05)
            
    except Exception as e:
         sensor.send_msg({'type': 'log', 'level': 'error', 'msg': f"IMU Read Error: {e}"})
    finally:
        sensor.shutdown()

if __name__ == "__main__":
    main(None, "bicycleimu", {})
