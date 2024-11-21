from servo import Servo
from machine import Pin, PWM
import ujson
import time
import sys

# Initialize the servos
servos = [Servo(pin=p) for p in range(8)]

while True:
    command = sys.stdin.readline().strip()
    if command:
        try:
            command_data = ujson.loads(command)
            for i, angle in enumerate(command_data):
                servos[i].move(angle)
        except ValueError:
            print("Error decoding JSON\r\n")
    time.sleep(0.1)

