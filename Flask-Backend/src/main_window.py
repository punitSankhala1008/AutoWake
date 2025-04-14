# src/main_window.py

import sys
import cv2
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont

# Import your detection and voice modules (ensure they are in the same folder)
from drowsiness_detector import DrowsinessDetector
from voice_assistant import VoiceAssistant

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Driver Drowsiness Detection")
        self.setGeometry(100, 100, 800, 600)

        # Video display label
        self.video_label = QLabel(self)
        self.video_label.resize(800, 500)

        # Status label for detection status
        self.status_label = QLabel("Status: Normal", self)
        self.status_label.setFont(QFont("Arial", 16))
        self.status_label.setStyleSheet("color: green;")

        # Start/Stop detection button
        self.start_button = QPushButton("Start Detection", self)
        self.start_button.setFont(QFont("Arial", 14))
        self.start_button.clicked.connect(self.start_detection)

        # Layout setup
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_label)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.start_button)
        bottom_layout.addWidget(self.status_label)
        main_layout.addLayout(bottom_layout)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Timer for frame updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = None  # OpenCV video capture object

        # Initialize the detection and voice assistant objects
        self.detector = DrowsinessDetector()
        self.voice = VoiceAssistant()
        self.last_alert_time = 0
        self.alert_interval = 5  # Minimum seconds between voice alerts

    def start_detection(self):
        """
        Toggle the webcam feed and detection process.
        """
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open webcam.")
                return
            self.start_button.setText("Stop Detection")
            self.timer.start(30)  # Update every 30 ms (~30 FPS)
        else:
            self.timer.stop()
            self.cap.release()
            self.cap = None
            self.start_button.setText("Start Detection")
            self.video_label.clear()
            self.status_label.setText("Status: Normal")
            self.status_label.setStyleSheet("color: green;")

    def update_frame(self):
        """
        Capture a frame from the webcam, process it for drowsiness detection,
        update the status label, and display the annotated video.
        """
        ret, frame = self.cap.read()
        if ret:
            # Pass the frame to your drowsiness detector
            is_drowsy, processed_frame = self.detector.detect_drowsiness(frame)
            current_time = time.time()
            if is_drowsy and (current_time - self.last_alert_time >= self.alert_interval):
                # Trigger voice alert if detection is positive and cooldown period has passed
                self.voice.speak("Warning: You appear to be drowsy. Please stay alert!")
                self.last_alert_time = current_time

            # Update status label based on detection
            if is_drowsy:
                self.status_label.setText("Status: Drowsy!")
                self.status_label.setStyleSheet("color: red;")
            else:
                self.status_label.setText("Status: Normal")
                self.status_label.setStyleSheet("color: green;")

            # Convert processed frame from BGR to RGB for display
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = processed_frame.shape
            bytes_per_line = ch * w
            q_img = QImage(processed_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))
        else:
            self.timer.stop()

if __name__ == "__main__":
    # For testing directly from main_window.py
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
