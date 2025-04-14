# Drowsiness Detection Application

This project implements a drowsiness detection application using computer vision and machine learning techniques. The application analyzes video frames from a webcam to detect signs of drowsiness in drivers by monitoring eye and mouth states.

## Project Structure

```
DrowsinessDetectionApp
├── src
│   ├── main_window.py          # User interface for the application using PyQt
│   ├── drowsiness_detector.py   # Drowsiness detection logic
│   ├── train_model.py           # Model training script
│   ├── voice_assistant.py        # Voice alert functionality
│   └── utils
│       └── helper_functions.py   # Utility functions for various tasks
├── models
│   ├── eye_model.h5             # Trained model for eye state detection
│   ├── mouth_model.h5            # Trained model for mouth state detection
│   └── shape_predictor_68_face_landmarks.dat  # Facial landmark detection model
├── datasets
│   ├── eyes
│   │   ├── open                 # Images of open eyes
│   │   └── closed               # Images of closed eyes
│   └── mouth
│       ├── yawn                 # Images of yawning mouths
│       └── no_yawn              # Images of non-yawning mouths
├── requirements.txt              # Project dependencies
├── README.md                     # Project documentation
└── setup.py                      # Packaging script
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd DrowsinessDetectionApp
   ```

2. **Install dependencies**:
   Create a virtual environment and install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Download the datasets**:
   Ensure that the datasets are placed in the `datasets` directory as specified in the project structure.

4. **Run the application**:
   Execute the main application file:
   ```
   python src/main_window.py
   ```

## Usage

- Start the application and click on the "Start Detection" button to begin monitoring for drowsiness.
- The application will provide voice alerts if drowsiness is detected based on eye and mouth states.

## Models and Datasets

- The eye detection model (`eye_model.h5`) is trained to classify images of open and closed eyes.
- The mouth detection model (`mouth_model.h5`) is trained to classify images of yawning and non-yawning mouths.
- The `shape_predictor_68_face_landmarks.dat` file is used for facial landmark detection, which is crucial for accurately identifying eye and mouth regions.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.