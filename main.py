from servo import Servo
from machine import Pin, PWM
import ujson
import time
import sys

servos = [Servo(pin=p) for p in range(8)]

while True:
    """Main loop to handle commands and control servos.

    Continuously listens for JSON encoded commands via stdin, decodes the commands and updates the positions of the connected servos.

    If a decoding error occurs, an error message is printed.

    """
    command = sys.stdin.readline().strip()
    if command:
        try:
            command_data = ujson.loads(command)
            for i, angle in enumerate(command_data):
                servos[i].move(angle)
        except ValueError:
            print("Error decoding JSON\r\n")
    time.sleep(0.1)

