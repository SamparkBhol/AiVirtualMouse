# AI Virtual Mouse Project 🖱️

I've created a virtual mouse system that lets you control your computer's cursor using hand gestures captured through your webcam. No physical mouse required - just your hand movements in the air!

## What I Built 🛠️

I developed this project to explore the intersection of computer vision and human-computer interaction. Using your webcam, the system:
- Tracks your hand movements in real-time
- Converts hand gestures into mouse actions
- Supports both cursor movement and clicking
- Runs smoothly with optimized performance

## How It Works 🤔

The system uses two main gestures:
1. **Moving the Cursor**: Hold up just your index finger and move it around
2. **Clicking**: Hold up both index and middle fingers, then pinch them together

Under the hood, I'm using:
- MediaPipe for hand landmark detection
- OpenCV for image processing
- PyAutoGUI for controlling the mouse
- Custom smoothing algorithms for precise movement

## Prerequisites 📋

Before you run my project, make sure you have:
- Python 3.7+
- A webcam
- The following Python packages:
  ```
  opencv-python
  mediapipe
  numpy
  pyautogui
  ```

## Installation 💻

1. Clone my repository:
   ```bash
   git clone https://github.com/yourusername/ai-virtual-mouse.git
   cd ai-virtual-mouse
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use 🚀

1. Run the main script:
   ```bash
   python AiVirtualMouse.py
   ```

2. Position yourself in front of your webcam
3. Use these gestures:
   - ☝️ Index finger up: Move cursor
   - ✌️ Index + Middle fingers up + pinch: Click
4. Press 'q' to quit the program

## Project Structure 📁

```
ai-virtual-mouse/
├── HandTrackingModule.py    # Hand detection and tracking implementation
├── AiVirtualMouse.py        # Main application file
└── README.md                # You are here!
```

## Key Features ✨

I've implemented several features to make this virtual mouse practical and user-friendly:
- Smooth cursor movement with custom interpolation
- Frame reduction to define an active area
- FPS counter to monitor performance
- Failsafe prevention for PyAutoGUI
- Visual feedback for all actions

## Limitations and Future Improvements 🔄

I'm aware of some current limitations:
- Works best in good lighting conditions
- Requires stable webcam positioning
- May need sensitivity adjustment for different users

I'm planning to add:
- Right-click functionality
- Drag-and-drop support
- Gesture customization
- Better smoothing algorithms
- Multi-monitor support

## Troubleshooting 🔧

If you encounter issues:

1. **Camera not working**: Try changing the camera index in `AIVirtualMouse.py`:
   ```python
   self.cap = cv2.VideoCapture(1)  # Try different numbers (0, 1, 2...)
   ```

2. **Jerky movements**: Adjust the smoothening value:
   ```python
   self.smoothening = 7  # Increase for smoother movement
   ```

3. **Detection issues**: Try adjusting lighting or camera position

## Contributing 🤝

I welcome contributions! If you'd like to improve this project:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License 📝

This project is licensed under the MIT License - feel free to use it however you'd like!

## Acknowledgments 👏

- MediaPipe team for their excellent hand tracking solution
- OpenCV community for the computer vision tools
- PyAutoGUI developers for the mouse control interface

## Contact 📫

Found a bug? Have a feature request? Feel free to:
- Open an issue
- Submit a pull request
- Connect with me on [GitHub](https://github.com/yourusername)

Happy virtual mousing! 🖱️✨
