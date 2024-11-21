import tkinter as tk
from tkinter import *
import json
import serial
import time

class Servo:
    """Represents a servo motor in the GUI."""
    def __init__(self, parent, servo_id, name, x, y, min_val=0, max_val=180):
        """Initialize a servo control in the GUI at specific pixel coordinates."""
        self.servo_id = servo_id
        self.name = name
        self.value = DoubleVar()

        self.label = Label(parent, text=name, font=("Arial", 12, "bold"), bg="#EAB8E4")
        self.label.place(x=x, y=y)

        self.slider = Scale(parent, from_=min_val, to=max_val, variable=self.value)
        self.slider.place(x=x, y=y + 30)    

    def get_value(self):
        """Get the current value of the servo."""
        return self.value.get()

    def set_value(self, value):
        """Set the value of the servo."""
        self.value.set(value)

class Leg:
    """Represents a single leg of the quadruped, containing two servos."""
    def __init__(self, parent, leg_id, name1, name2, x1, y1, x2, y2):
        """Initialize a leg with two servos."""
        self.servo1 = Servo(parent, leg_id * 2, name1, x1, y1)
        self.servo2 = Servo(parent, leg_id * 2 + 1, name2, x2, y2)

    def get_values(self):
        """Get the positions of both servos in the leg."""
        return [self.servo1.get_value(), self.servo2.get_value()]

    def set_values(self, values):
        """Set the positions of both servos in the leg."""
        self.servo1.set_value(values[0])
        self.servo2.set_value(values[1])

class Quadruped:
    """Represents the entire quadruped robot with legs and servos."""
    def __init__(self, parent):
        """Initialize the quadruped with four legs, each with two servos."""
        positions = [
            ("Top Left Hip", "Bottom Left Hip", 50, 20, 50, 170),  
            ("Top Right Hip", "Bottom Right Hip", 250, 20, 250, 170),  
            ("Top Left Leg", "Bottom Left Leg", 50, 320, 50, 470),  
            ("Top Right Leg", "Bottom Right Leg", 250, 320, 250, 470)]
        
        self.legs = [Leg(parent, i, name1, name2, x1, y1, x2, y2) for i, (name1, name2, x1, y1, x2, y2) in enumerate(positions)]

    def get_all_positions(self):
        """Get the positions of all servos in the quadruped."""
        return [servo_value for leg in self.legs for servo_value in leg.get_values()]

    def set_all_positions(self, positions):
        """Set positions of all servos in the quadruped."""
        for leg, position in zip(self.legs, positions):
            leg.set_values(position)

class StateManager:
    """Manages saving and loading of robot states."""
    def __init__(self):
        """Initialize the state manager."""
        self.states = {}  # do i even need this here?

    def load_states(self, filename):
        """Load states from a file and populate the internal states dictionary."""
        try:
            with open(filename, "r") as f:
                self.states = json.load(f)  
                print("States loaded successfully.")
        except FileNotFoundError:
            print("Error: No saved states found.")
            self.states = {}  

    def save_states(self, filename):
        """Save all states to a file from the internal states dictionary."""
        with open(filename, "w") as f:
            json.dump(self.states, f)  
            print("States saved successfully.")

    def get_state(self, name):
        """Get a specific state by name."""
        if name in self.states:
            return self.states[name]  
        else:
            print(f"Error: State '{name}' not found.")
            return None

    def set_state(self, name, state):
        """Set a specific state by name."""
        self.states[name] = state  
        print(f"State '{name}' set successfully.")

class SerialCommunicator:
    """Handles serial communication with the Pico."""
    def __init__(self, port='COM5', baud_rate=9600):
        """Initialize the serial connection."""
        self.port = port
        self.baud_rate = baud_rate
            
    def open_serial(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            print(f"Connected to {self.port} at {self.baud_rate} baud.")
        except serial.SerialException:
            print("Serial Error: Failed to connect to the serial port.")
            self.ser = None  
        
    def close(self):
        """Close the serial port."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Disconnected from {self.port}")
            
    def send_command(self, command):
        """Send a command to the Pico."""
        self.open_serial()
        if self.ser and self.ser.is_open:
            try:
                command_json = json.dumps(command) + "\r\n"
                self.ser.write(command_json.encode())
                print("Sending:", command_json)
                time.sleep(0.5) 
                if self.ser.in_waiting > 0:
                    response = self.ser.readline().decode('utf-8').strip()
                    print("Received from Pico:", response)
                self.close()
                return True
            except serial.SerialException:
                print("Serial Error: Failed to send command.")
                self.close()
                return False
        else:
            print("Serial port is not open.")
            return False

class QuadrupedGUI: 
    """Main GUI class for controlling the spider robot."""
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Spider Robot Servo Controller")
        self.root.geometry("820x720")
        self.light_purple = "#EAB8E4"
        self.root.configure(bg=self.light_purple)

        self.servo_vars = [DoubleVar() for _ in range(8)]
        self.serial_communicator = SerialCommunicator(port='COM5', baud_rate=9600)  

        self.create_widgets()

    def create_widgets(self):
        """Create and arrange the GUI elements."""
        left_frame = Frame(self.root, bg=self.light_purple)
        right_frame = Frame(self.root, bg=self.light_purple)

        left_frame.grid(row=0, column=0, padx=40, pady=(40, 20))
        right_frame.grid(row=0, column=1, padx=40, pady=(40, 20))

        left_group1 = Frame(left_frame, bd=2, relief='raised')
        left_group2 = Frame(left_frame, bd=2, relief='raised')
        right_group1 = Frame(right_frame, bd=2, relief='raised')
        right_group2 = Frame(right_frame, bd=2, relief='raised')

        left_group1.pack(padx=10, pady=10, fill='both', expand=True)
        left_group2.pack(padx=10, pady=10, fill='both', expand=True)
        right_group1.pack(padx=10, pady=10, fill='both', expand=True)
        right_group2.pack(padx=10, pady=10, fill='both', expand=True)

        for i in range(4):
            self.create_servo_control(left_group1 if i < 2 else right_group1, i)

        for i in range(4, 8):
            self.create_servo_control(left_group2 if i < 6 else right_group2, i)

        Button(self.root, text="Show Servo Values", command=self.show_values, bg="white", fg="black", font=("Arial", 12, "bold")).grid(row=1, column=0, columnspan=2, pady=5)
        Button(self.root, text="Send Values to Pico", command=self.send_values, bg="white", fg="black", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=2, pady=5)
        Button(self.root, text="Save State", command=self.save_state, bg="white", fg="black", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=5)
        Button(self.root, text="Load State", command=self.load_state, bg="white", fg="black", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=5)

        self.display_label = Label(self.root, text="", bg=self.light_purple, font=("Arial", 12))  # Set same bg color
        self.display_label.grid(row=6, column=0, columnspan=2)

    def create_servo_control(self, parent, index):
        """Create a label and scale for a servo."""
        Label(parent, text=f"Servo {index + 1}", font=("Arial", 12, "bold")).pack()
        Scale(parent, from_=0, to=180, orient=HORIZONTAL, variable=self.servo_vars[index], 
              troughcolor=self.light_purple, sliderlength=30, length=300).pack()

    def show_values(self):
        """Display current servo values."""
        values = ""
        for i in range(8):
            values += f"Servo {i + 1}: {self.servo_vars[i].get()}\n"
        self.display_label.config(text=values)

    def save_state(self):
        """Save current slider values to a JSON file."""
        state = {f"Servo {i + 1}": self.servo_vars[i].get() for i in range(8)}
        with open('robot_state.json', 'w') as f:
            json.dump(state, f)
        self.display_label.config(text="State saved")

    def load_state(self):
        """Load slider values from a JSON file."""
        try:
            with open('robot_state.json', 'r') as f:
                state = json.load(f)
                for i in range(8):
                    self.servo_vars[i].set(state[f"Servo {i + 1}"])
                self.display_label.config(text="State loaded")
        except FileNotFoundError:
            self.display_label.config(text="No saved state found.")
        except (json.JSONDecodeError, KeyError):
            self.display_label.config(text="Error loading, invalid file format.")

    def send_values(self):
        """Send servo values to the Raspberry Pi Pico."""
        servo_values = [self.servo_vars[i].get() for i in range(8)]
        if self.serial_communicator.send_command(servo_values):
            self.display_label.config(text=servo_values)
        else:
            self.display_label.config(text="Failed to connect to the serial port.")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = QuadrupedGUI(root)
    root.mainloop()
