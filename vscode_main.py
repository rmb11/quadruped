import tkinter as tk
from tkinter import *
from tkinter import ttk  
import json
import serial
import time


class Servo:
    """Represents a servo motor in the GUI.
    
        Attributes:
        servo_id (int): ID of the servo.
        name (str): Name of the servo.
        value (DoubleVar): Current value of the servo.
        label (Label): Label for the servo in the GUI.
        slider (Scale): Slider to control the servo position in the GUI.
    """
        
    def __init__(self, parent, servo_id, name, x, y, min_val=0, max_val=180):
        """Initialises a Servo instance.

        Args:
            parent (Frame): Parent frame in which the servo is displayed.
            servo_id (int): ID of the servo.
            name (str): Name of the servo.
            x (int): X coordinate for the servo's GUI placement.
            y (int): Y coordinate for the servo's GUI placement.
            min_val (int, optional): Minimum value for the slider, defaults to 0.
            max_val (int, optional): Maximum value for the slider, defaults to 180.
        """    
        self.servo_id = servo_id
        self.name = name
        self.value = DoubleVar()

        self.label = Label(parent, text=name, font=("Arial", 12, "bold"), bg="#EAB8E4")
        self.label.place(x=x, y=y)

        self.slider = Scale(parent, from_=min_val, to=max_val, variable=self.value)
        self.slider.place(x=x, y=y + 30)

    def get_value(self):
        """Gets the current value of the servo.

        Returns:
            float: Current value of the servo.
        """
        return self.value.get()

    def set_value(self, value):
        """Sets the value of the servo.

        Args:
            value (float): New value for the servo.
        """
        self.value.set(value)


class Leg:
    """Represents a single leg of the quadruped, containing two servos."
    
    Attributes:
        servo1 (Servo): First servo in the leg.
        servo2 (Servo): Second servo in the leg. """
    def __init__(self, parent, leg_id, name1, name2, x1, y1, x2, y2):
        """Initialises a Leg instance.

        Args:
            parent (Frame): Parent frame in which the leg is displayed.
            leg_id (int): ID of the leg.
            name1 (str): Name of the first servo in the leg.
            name2 (str): Name of the second servo in the leg.
            x1 (int): X coordinate for the first servo's GUI placement.
            y1 (int): Y coordinate for the first servo's GUI placement.
            x2 (int): X coordinate for the second servo's GUI placement.
            y2 (int): Y coordinate for the second servo's GUI placement.
        """
        self.servo1 = Servo(parent, leg_id * 2, name1, x1, y1)
        self.servo2 = Servo(parent, leg_id * 2 + 1, name2, x2, y2)

    def get_values(self):
        """Gets the positions of both servos in the leg.

        Returns:
            list[float]: List of the positions of the two servos.
        """
        return [self.servo1.get_value(), self.servo2.get_value()]

    def set_values(self, values):
        """Sets the positions of both servos in the leg.

        Args:
            values (list[float]): List containing new positions for both servos.
        """
        self.servo1.set_value(values[0])
        self.servo2.set_value(values[1])


class Quadruped:
    """Represents the entire quadruped robot with legs and servos.

    Attributes:
        legs (list[Leg]): A list of the robot's four legs, each with two servos.
    """
    def __init__(self, parent):
        """Initialises a quadruped instance.
        
        Args:
            parent (Frame): Parent frame where the quadruped is displayed
        """
        positions = [
            ("Top Left Hip", "Bottom Left Hip", 50, 20, 50, 170),
            ("Top Right Hip", "Bottom Right Hip", 250, 20, 250, 170),
            ("Top Left Leg", "Bottom Left Leg", 50, 320, 50, 470),
            ("Top Right Leg", "Bottom Right Leg", 250, 320, 250, 470),
        ]

        self.legs = [
            Leg(parent, i, name1, name2, x1, y1, x2, y2)
            for i, (name1, name2, x1, y1, x2, y2) in enumerate(positions)
        ]

    def get_all_positions(self):
        """Gets the positions of all servos in the quadruped.

        Returns:
            list[float]: List of positions for all servos.
        """
        return [servo_value for leg in self.legs for servo_value in leg.get_values()]

    def set_all_positions(self, positions):
        """Sets the positions of all servos in the quadruped.

        Args:
            positions (list[float]): List of new positions for all servos.
        """
        for leg, position in zip(self.legs, positions):
            leg.set_values(position)


class StateManager:
    """Manages saving and loading of robot states.

    Attributes:
        filename (str): Filename where states are saved.
        states (dict): Dictionary of saved states.
    """
    def __init__(self, filename="robot_states.json"):
        """Initialises a StateManager instance.

        Args:
            filename (str, optional): Filename for saving/loading states. Defaults to "robot_states.json".
        """
        self.filename = filename
        self.states = self.load_states()

    def load_states(self):
        """Loads states from the JSON file.

        Returns:
            dict: Dictionary of saved states.
        """
        try:
            with open(self.filename, "r") as f:
                states = json.load(f)
                print("States loaded successfully.")
                return states
        except (FileNotFoundError, json.JSONDecodeError):
            print("No valid saved states found.")
            return {}

    def save_states(self):
        """Save all states to the JSON file."""
        with open(self.filename, "w") as f:
            json.dump(self.states, f)
            print("States saved successfully.")

    def get_state(self, name):
        """Gets a specific state by name.

        Args:
            name (str): Name of the state.

        Returns:
            dict or None: The state data if it exists, otherwise None.
        """
        return self.states.get(name, None)

    def set_state(self, name, state):
        """Sets (saves) a specific state by name.

        Args:
            name (str): Name of the state.
            state (dict): State data to save.
        """
        self.states[name] = state
        self.save_states()
        print(f"State '{name}' saved successfully.")

    def get_all_state_names(self):
        """Gets a list of all saved state names.

        Returns:
            list[str]: List of saved state names.
        """
        return list(self.states.keys())


class SerialCommunicator:
    """Handles serial communication with the Pico.
    Attributes:
        port (str): The serial port to use.
        baud_rate (int): Baud rate for the serial connection.
    """
    def __init__(self, port='COM5', baud_rate=9600):
        """Initialises a SerialCommunicator instance.

        Args:
            port (str, optional): The serial port.
            baud_rate (int, optional): The baud rate.
        """
        self.port = port
        self.baud_rate = baud_rate

    def open_serial(self):
        """Opens the serial connection."""

        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            print(f"Connected to {self.port} at {self.baud_rate} baud.")
        except serial.SerialException:
            print("Serial Error: Failed to connect to the serial port.")
            self.ser = None

    def close(self):
        """Closes the serial connection."""

        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Disconnected from {self.port}")

    def send_command(self, command):
        """Sends a command to the Pico.

        Args:
            command (dict): The command data to send.

        Returns:
            bool: True if the command sent successfully, otherwise False.
        """
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
    """Main GUI class for controlling the quadruped robot.

    Attributes:
        root (Tk): The root Tkinter window.
        servo_vars (list[DoubleVar]): List of DoubleVars representing positions of the servos.
        serial_communicator (SerialCommunicator): Handles communication with the Pico.
        state_manager (StateManager): Manages saving and loading of robot states.
        state_name_entry (Entry): Input field for entering the name of a new state.
        state_dropdown (ttk.Combobox): Dropdown for selecting saved states.
        display_label (Label): Label for displaying messages in the GUI.
    """
    def __init__(self, root):
        """Initializes the GUI for the quadruped robot.

        Args:
            root (Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Spider Robot Servo Controller")
        self.root.geometry("820x720")
        self.light_purple = "#EAB8E4"
        self.root.configure(bg=self.light_purple)

        self.servo_vars = [DoubleVar() for _ in range(8)]
        self.serial_communicator = SerialCommunicator(port='COM5', baud_rate=9600)
        self.state_manager = StateManager()

        self.create_gui()
        self.update_state_dropdown()

    def create_gui(self):
        """Creates the widgets for the GUI, including servo sliders, state controls and action buttons."""
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

        state_frame = Frame(self.root, bg=self.light_purple)
        state_frame.grid(row=1, column=0, columnspan=2, pady=10)

        Label(state_frame, text="State Name:", font=("Arial", 12, "bold"), bg=self.light_purple).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.state_name_entry = Entry(state_frame, font=("Arial", 12), width=20)
        self.state_name_entry.grid(row=0, column=1, padx=5, pady=5)
        Button(state_frame, text="Save State", command=self.save_state, bg="white", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5)

        Label(state_frame, text="Load State:", font=("Arial", 12, "bold"), bg=self.light_purple).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.state_dropdown = ttk.Combobox(state_frame, state="readonly", width=25)
        self.state_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.state_dropdown.bind("<<ComboboxSelected>>", self.load_state)

        Button(self.root, text="Show Servo Values", command=self.show_values, bg="white", fg="black", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=2, pady=5)
        Button(self.root, text="Send Values to Pico", command=self.send_values, bg="white", fg="black", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=5)

        self.display_label = Label(self.root, text="", bg=self.light_purple, font=("Arial", 12))
        self.display_label.grid(row=4, column=0, columnspan=2)

    def create_servo_control(self, parent, index):
        """Creates a slider control for a servo.

        Args:
            parent (Frame): Parent frame where the slider will be placed.
            index (int): Index of the servo.
        """
        Label(parent, text=f"Servo {index + 1}", font=("Arial", 12, "bold")).pack()
        Scale(parent, from_=0, to=180, orient=HORIZONTAL, variable=self.servo_vars[index], sliderlength=30, length=300).pack()

    def save_state(self):
        """Saves the current servo positions as a new state."""
        state_name = self.state_name_entry.get().strip()
        if not state_name:
            self.display_label.config(text="State name cannot be empty!")
            return

        current_state = {f"Servo {i + 1}": self.servo_vars[i].get() for i in range(8)}
        self.state_manager.set_state(state_name, current_state)
        self.update_state_dropdown()
        self.display_label.config(text=f"State '{state_name}' saved successfully.")

    def load_state(self, event=None):
        """Loads a saved state and updates the servo sliders.

        Args:
            event (Event, optional): The event triggered by selecting a dropdown option. Defaults to None.
        """
        selected_state = self.state_dropdown.get()
        state = self.state_manager.get_state(selected_state)
        if state:
            for i in range(8):
                self.servo_vars[i].set(state[f"Servo {i + 1}"])
            self.display_label.config(text=f"State '{selected_state}' loaded.")
        else:
            self.display_label.config(text="Error loading state.")

    def update_state_dropdown(self):
        """Updates the dropdown with the list of saved states"""
        self.state_dropdown["values"] = self.state_manager.get_all_state_names()

    def show_values(self):
        """Displays the current servo values in the GUI"""
        values = "\n".join([f"Servo {i + 1}: {self.servo_vars[i].get()}" for i in range(8)])
        self.display_label.config(text=values)

    def send_values(self):
        """Sends the current servo values to the Pico"""
        servo_values = [self.servo_vars[i].get() for i in range(8)]
        if self.serial_communicator.send_command(servo_values):
            self.display_label.config(text="Values sent to Pico.")
        else:
            self.display_label.config(text="Failed to send values to Pico.")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuadrupedGUI(root)
    root.mainloop()
