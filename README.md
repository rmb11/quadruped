# Quadruped

A project to control a quadruped robot using a Python GUI and Raspberry Pi Pico.

---

## Project Description

This project involves implementing a control system for a quadruped robot with servo-controlled legs. The system consists of two main components:

1. **Graphical User Interface (GUI):** Running on a PC for user interaction.
2. **Controller:** Running on a Raspberry Pi Pico microcontroller to control the robot's servos.

The system allows users to control the robot's servos, save and load robot states, and communicate between the PC and the Pico.

---

## Features

### Graphical User Interface (GUI)
- Slider controls for setting servo angles.
- Dropdown menu to load predefined states.

### State Management
- Save robot poses as JSON files.
- Load and apply saved states in real time.

### Hardware Control
- Real-time communication with the Raspberry Pi Pico.
- Smooth servo transitions for precise movements.

### Customizable Settings
- Ability to reconfigure servo ranges and angles.

---

## Setup Instructions

1. **Clone repository**
   ```bash
   git clone https://github.com/rmb11/quadruped.git
   cd quadruped

2. **Prepare Raspberry Pico**
- Install latest MicroPython firmware.
- Open Thonny and connect Pico.
- Copy the following files to the Pico: main.py and servo.py

3. **Install pyserial**
   ```bash
   pip install pyserial

4. **Run GUI**
   ```bash
   cd path/to/quadrupedfolder
   python vscodemain.py

## Demo Video
[![Demo Video](https://img.youtube.com/vi/VrJfyDyFLqI/0.jpg)](https://youtube.com/shorts/VrJfyDyFLqI?si=_aOQxeyFzYjAQ-8Y)

## External Libraries and Dependencies

This project uses several external libraries to handle different functionalities. Below is a list of the libraries, their purpose, licenses, and installation instructions.

### Python Libraries (PC-Side)
1. **`pyserial`**
   - **Purpose:** For serial communication between the PC and the Raspberry Pi Pico.
   - **License:** [Python Software Foundation License (PSFL)](https://docs.python.org/3/license.html)
   - **Installation:** Run the following command:
     ```bash
     pip install pyserial
     ```

2. **`tkinter`**
   - **Purpose:** Provides the graphical user interface (GUI) for controlling the quadruped robot.
   - **License:** [Python Software Foundation License (PSFL)](https://docs.python.org/3/license.html)
   - **Note:** This library is included with Python on most systems and does not require installation.

3. **`json`**
   - **Purpose:** Used for state saving and loading of robot states.
   - **License:** [Python Software Foundation License (PSFL)](https://docs.python.org/3/license.html)
   - **Note:** This is a built-in Python library and no additional installation is needed.

4. **`time`**
   - **Purpose:** Adds delays and time functionalities in the scripts.
   - **License:** [Python Software Foundation License (PSFL)](https://docs.python.org/3/license.html)
   - **Note:** This is a built-in Python library.

---

### MicroPython Libraries (Pico-Side)
1. **`machine`**
   - **Purpose:** Provides access to GPIO pins and PWM for servo control.
   - **License:** [MIT License](https://github.com/micropython/micropython/blob/master/LICENSE)
   - **Installation:** Included with MicroPython.

2. **`ujson`**
   - **Purpose:** Handles JSON encoding and decoding for command processing.
   - **License:** [MIT License](https://github.com/micropython/micropython/blob/master/LICENSE)
   - **Installation:** Included with MicroPython.

3. **`sys`**
   - **Purpose:** Allows reading from standard input (`stdin`) for receiving commands on the Pico.
   - **License:** [MIT License](https://github.com/micropython/micropython/blob/master/LICENSE)
   - **Installation:** Included with MicroPython.

4. **`time`**
   - **Purpose:** Adds delay functionality in the main control loop.
   - **License:** [MIT License](https://github.com/micropython/micropython/blob/master/LICENSE)
   - **Installation:** Included with MicroPython.

---

### Licenses
- **Project License:** This project is licensed under the [MIT License](LICENSE).
- Each library's license is linked above for reference.
