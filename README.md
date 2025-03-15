# Real-Time Gesture Controlled Cursor and Arrow Key Interface

## Description
This project implements a gesture-based control system using OpenCV, MediaPipe, and PyAutoGUI. It enables users to control their computer mouse and keyboard using hand gestures detected via a webcam.

## Features
- **Mouse Control:** Left hand movements control the mouse pointer, and finger gestures simulate clicks.
- **Keyboard Control:** Right-hand gestures simulate arrow key presses for navigation.
- **Real-Time Gesture Recognition:** Uses MediaPipe Hands for detecting hand landmarks.
- **Latency:** Displays real-time processing latency on the screen.

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/your-repository.git
2. Install dependencies:
   ```sh
   pip install opencv-python mediapipe pyautogui
3. Run the script:
   ```sh
   python main.py
## Requirements
- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI
- Webcam

## Usage
1. Ensure your webcam is connected
2. Run the script:
   ```sh
   python main.py
3. Control your system using hand gestures:
- Move the mouse with your left hand.
- Click by bringing your index finger down.
- Control arrow keys with your right hand swipes.

## Contributing
Pull requests are welcome! If you'd like to contribute, please fork the repository and create a new branch.
