# # # Flask-Backend/server.py

# # import os
# # import sys

# # # Add the 'src' folder (relative to this file) to sys.path
# # src_path = os.path.join(os.path.dirname(__file__), "src")
# # if src_path not in sys.path:
# #     sys.path.append(src_path)

# # # Flask-Backend/server.py

# # from flask import Flask, request, jsonify
# # import base64
# # import cv2
# # import numpy as np
# # from src.drowsiness_detector import DrowsinessDetector

# # app = Flask(__name__)
# # detector = DrowsinessDetector()


# # @app.route('/detect', methods=['POST'])
# # def detect():
# #     data = request.get_json()
# #     image_b64 = data.get("image")
# #     if not image_b64:
# #         return jsonify({"error": "No image provided"}), 400

# #     # Decode base64 image
# #     img_bytes = base64.b64decode(image_b64)
# #     np_arr = np.frombuffer(img_bytes, np.uint8)
# #     frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
# #     # Run detection
# #     is_drowsy, processed_frame = detector.detect_drowsiness(frame)
    
# #     # For simplicity, return detection status only
# #     return jsonify({"drowsy": is_drowsy})

# # if __name__ == '__main__':
# #     app.run(host='127.0.0.1', port=5000)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from src.drowsiness_detector import DrowsinessDetector

# app = Flask(__name__)
# CORS(app)  # Allow cross-origin requests from Electron

# detector = DrowsinessDetector()

# @app.route('/start-detection', methods=['POST'])
# def start_detection():
#     try:
#         # Simulate detection logic
#         is_drowsy = detector.detect_drowsiness()  # Replace with actual detection logic
#         return jsonify({"drowsy": is_drowsy})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, Response, jsonify
import cv2
import time
from src.drowsiness_detector import DrowsinessDetector
from src.voice_assistant import VoiceAssistant

app = Flask(__name__)

# Initialize detector and voice assistant
detector = DrowsinessDetector()
voice = VoiceAssistant()

# Initialize webcam
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not video_capture.isOpened():
    raise RuntimeError("Error: Could not open webcam.")

# Shared state for drowsiness status
drowsy_state = {
    "drowsy": False,
    "blink_count": 0,
    "yawn_count": 0
}
last_alert_time = 0
alert_interval = 2  # Seconds between alerts

def generate_frames():
    """Generate annotated frames for streaming."""
    target_fps = 30
    frame_delay = 1 / target_fps

    while True:
        success, frame = video_capture.read()
        if not success:
            print("Error: Could not read frame.")
            break

        # Detect drowsiness
        is_drowsy, processed_frame = detector.detect_drowsiness(frame)

        # Update drowsy_state
        drowsy_state["drowsy"] = is_drowsy
        drowsy_state["blink_count"] = detector.blink_count
        drowsy_state["yawn_count"] = detector.yawn_count

        # Trigger voice alert every time drowsiness is detected
        if is_drowsy:
            print("Warning: Drowsiness detected!")
            voice.speak("Warning: You appear to be drowsy. Please stay alert!")

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        time.sleep(frame_delay)

@app.route('/video')
def video_feed():
    """Stream the processed video feed."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def get_status():
    """Return drowsiness status."""
    return jsonify(drowsy_state)

def cleanup():
    """Release resources."""
    video_capture.release()

if __name__ == '__main__':
    try:
        app.run(host='localhost', port=5000, threaded=True)
    finally:
        cleanup()