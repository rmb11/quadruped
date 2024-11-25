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

