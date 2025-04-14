import cv2
import time
from drowsiness_detector import DrowsinessDetector
from voice_assistant import VoiceAssistant

def main():
    # Initialize the drowsiness detector and voice assistant
    detector = DrowsinessDetector()
    voice = VoiceAssistant()
    
    # Open the default webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Could not open webcam. Please check your camera or its drivers.")
        return

    target_fps = 30     # Target frames per second for smooth processing
    delay = int(1000 / target_fps)  # Delay in milliseconds
    alert_interval = 5  # Minimum time in seconds between alerts
    last_alert_time = 0 # Timestamp when the last alert was triggered

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame. Check if the webcam is functioning.")
            break

        # Get drowsiness status and the processed frame
        is_drowsy, processed_frame = detector.detect_drowsiness(frame)

        # Display the processed frame if available
        if processed_frame is not None:
            cv2.imshow("Drowsiness Detection", processed_frame)
        else:
            print("Warning: Processed frame is None.")

        # Trigger voice alert if drowsiness is detected and cooldown has elapsed
        current_time = time.time()
        if is_drowsy and (current_time - last_alert_time >= alert_interval):
            voice.speak("Warning: You appear to be drowsy. Please stay alert!")
            last_alert_time = current_time

        # Exit on pressing 'q'
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

