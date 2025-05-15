# import os
# import cv2
# import dlib
# import numpy as np
# import time
# from tensorflow.keras.models import load_model
# from collections import deque

# class DrowsinessDetectorLSTM:
#     def __init__(self):
#         # Get the directory path of this file
#         base_dir = os.path.dirname(os.path.abspath(__file__))

#         # Construct absolute paths to model files
#         predictor_path = os.path.join(base_dir, "models", "shape_predictor_68_face_landmarks.dat")
#         eye_model_path = os.path.join(base_dir, "models", "eye_model.h5")
#         mouth_model_path = os.path.join(base_dir, "models", "mouth_model.h5")
#         lstm_model_path = os.path.join(base_dir, "models", "lstm_model.h5")

#         # Check if model files exist
#         if not os.path.exists(predictor_path):
#             raise FileNotFoundError(f"Shape predictor file not found at {predictor_path}")
#         if not os.path.exists(eye_model_path):
#             raise FileNotFoundError(f"Eye model file not found at {eye_model_path}")
#         if not os.path.exists(mouth_model_path):
#             raise FileNotFoundError(f"Mouth model file not found at {mouth_model_path}")
#         if not os.path.exists(lstm_model_path):
#             raise FileNotFoundError(f"LSTM model file not found at {lstm_model_path}")

#         # Initialize face detector and landmark predictor
#         self.detector = dlib.get_frontal_face_detector()
#         self.predictor = dlib.shape_predictor(predictor_path)

#         # Load models
#         self.eye_model = load_model(eye_model_path)
#         self.mouth_model = load_model(mouth_model_path)
#         self.lstm_model = load_model(lstm_model_path)

#         # Detection parameters
#         self.sequence_length = 30  # Number of frames in sequence
#         self.state_sequence = deque(maxlen=self.sequence_length)  # Store eye/mouth states
#         self.blink_count = 0
#         self.yawn_count = 0
#         self.img_size = (64, 64)

#     def reset(self):
#         self.blink_count = 0
#         self.yawn_count = 0
#         self.drowsy = False


#     def preprocess_region(self, region):
#         """Preprocess the region for model input."""
#         region = cv2.resize(region, self.img_size)
#         region = region / 255.0
#         return np.expand_dims(region, axis=0)

#     def get_bounding_box(self, points, frame):
#         """Get bounding box for the given points with padding."""
#         x_coords, y_coords = zip(*points)
#         x_min, x_max = min(x_coords), max(x_coords)
#         y_min, y_max = min(y_coords), max(y_coords)
#         padding = 10
#         x_min = max(0, x_min - padding)
#         y_min = max(0, y_min - padding)
#         x_max = min(frame.shape[1], x_max + padding)
#         y_max = min(frame.shape[0], y_max + padding)
#         return (x_min, y_min, x_max, y_max)

#     def detect_drowsiness(self, frame):
#         """Detect drowsiness using LSTM and return status and annotated frame."""
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = self.detector(gray)

#         if len(faces) == 0:
#             return False, frame

#         drowsy = False

#         for face in faces:
#             landmarks = self.predictor(gray, face)

#             left_eye_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)]
#             right_eye_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)]
#             mouth_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)]

#             left_eye_coords = self.get_bounding_box(left_eye_pts, frame)
#             right_eye_coords = self.get_bounding_box(right_eye_pts, frame)
#             mouth_coords = self.get_bounding_box(mouth_pts, frame)

#             left_eye_region = frame[left_eye_coords[1]:left_eye_coords[3], left_eye_coords[0]:left_eye_coords[2]]
#             right_eye_region = frame[right_eye_coords[1]:right_eye_coords[3], right_eye_coords[0]:right_eye_coords[2]]
#             mouth_region = frame[mouth_coords[1]:mouth_coords[3], mouth_coords[0]:mouth_coords[2]]

#             if left_eye_region.size == 0 or right_eye_region.size == 0 or mouth_region.size == 0:
#                 continue

#             left_eye_input = self.preprocess_region(left_eye_region)
#             right_eye_input = self.preprocess_region(right_eye_region)
#             mouth_input = self.preprocess_region(mouth_region)

#             left_eye_pred = self.eye_model.predict(left_eye_input)
#             right_eye_pred = self.eye_model.predict(right_eye_input)
#             mouth_pred = self.mouth_model.predict(mouth_input)

#             left_eye_closed = np.argmax(left_eye_pred) == 1
#             right_eye_closed = np.argmax(right_eye_pred) == 1
#             is_yawning = np.argmax(mouth_pred) == 1

#             # Store state: [left_eye_closed, right_eye_closed, is_yawning]
#             state = [int(left_eye_closed), int(right_eye_closed), int(is_yawning)]
#             self.state_sequence.append(state)

#             # Count blinks and yawns for status reporting
#             if left_eye_closed and right_eye_closed:
#                 self.blink_count += 1
#                 print(f"[LSTM Blink] Count: {self.blink_count}")
#             if is_yawning:
#                 self.yawn_count += 1
#                 print(f"[LSTM Yawn] Count: {self.yawn_count}")

#             # Predict drowsiness with LSTM if sequence is full
#             if len(self.state_sequence) == self.sequence_length:
#                 sequence_array = np.array(self.state_sequence)
#                 sequence_array = np.expand_dims(sequence_array, axis=0)  # Shape: (1, sequence_length, 3)
#                 lstm_pred = self.lstm_model.predict(sequence_array)
#                 drowsy = np.argmax(lstm_pred, axis=1)[0] == 1
#                 if drowsy:
#                     print("LSTM: Drowsiness Detected.")
#                     cv2.putText(frame, "Drowsy!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#             # Draw rectangles
#             cv2.rectangle(frame, (left_eye_coords[0], left_eye_coords[1]),
#                           (left_eye_coords[2], left_eye_coords[3]), (0, 255, 0), 2)
#             cv2.rectangle(frame, (right_eye_coords[0], right_eye_coords[1]),
#                           (right_eye_coords[2], right_eye_coords[3]), (0, 255, 0), 2)
#             cv2.rectangle(frame, (mouth_coords[0], mouth_coords[1]),
#                           (mouth_coords[2], mouth_coords[3]), (0, 255, 0), 2)

#         return drowsy, frame


# src/drowsiness_detector_feature_lstm.py

import os
import cv2
import dlib
import numpy as np
import time
from tensorflow.keras.models import load_model
from collections import deque

class DrowsinessDetectorLSTM:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Model paths
        predictor_path   = os.path.join(base_dir, "models", "shape_predictor_68_face_landmarks.dat")
        eye_model_path   = os.path.join(base_dir, "models", "eye_model.h5")
        mouth_model_path = os.path.join(base_dir, "models", "mouth_model.h5")
        lstm_model_path  = os.path.join(base_dir, "models", "lstm_model.h5")

        # Ensure files exist
        for p in (predictor_path, eye_model_path, mouth_model_path, lstm_model_path):
            if not os.path.exists(p):
                raise FileNotFoundError(f"Missing: {p}")

        # Load detectors & models
        self.detector    = dlib.get_frontal_face_detector()
        self.predictor   = dlib.shape_predictor(predictor_path)
        self.eye_model   = load_model(eye_model_path)
        self.mouth_model = load_model(mouth_model_path)
        self.lstm_model  = load_model(lstm_model_path)

        # Sequence buffer for LSTM
        self.sequence_length = 30
        self.state_sequence  = deque(maxlen=self.sequence_length)

        # Counters and flags
        self.blink_count = 0    # <— define this!
        self.yawn_count  = 0    # <— and this!
        self.drowsy      = False

        # To avoid counting the same blink/yawn continuously
        self._prev_blink_state = False
        self._prev_yawn_state  = False

        self.img_size = (64, 64)

    def reset(self):
        """Clear everything when switching models."""
        self.state_sequence.clear()
        self.blink_count       = 0
        self.yawn_count        = 0
        self.drowsy            = False
        self._prev_blink_state = False
        self._prev_yawn_state  = False

    def preprocess_region(self, region):
        region = cv2.resize(region, self.img_size)
        region = region / 255.0
        return np.expand_dims(region, axis=0)

    def get_bounding_box(self, points, frame):
        x_coords, y_coords = zip(*points)
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        pad = 10
        x_min = max(0, x_min - pad)
        y_min = max(0, y_min - pad)
        x_max = min(frame.shape[1], x_max + pad)
        y_max = min(frame.shape[0], y_max + pad)
        return (x_min, y_min, x_max, y_max)

    def detect_drowsiness(self, frame):
        """Return (is_drowsy, annotated_frame)."""
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        self.drowsy = False

        for face in faces:
            lm = self.predictor(gray, face)

            # Collect landmarks
            def pts(start, end):
                return [(lm.part(i).x, lm.part(i).y) for i in range(start, end)]
            le_pts, re_pts, m_pts = pts(36,42), pts(42,48), pts(48,68)

            # Bounding boxes & ROIs
            le_bb = self.get_bounding_box(le_pts, frame)
            re_bb = self.get_bounding_box(re_pts, frame)
            m_bb  = self.get_bounding_box(m_pts, frame)

            le_roi = frame[le_bb[1]:le_bb[3], le_bb[0]:le_bb[2]]
            re_roi = frame[re_bb[1]:re_bb[3], re_bb[0]:re_bb[2]]
            m_roi  = frame[m_bb[1]:m_bb[3], m_bb[0]:m_bb[2]]

            if le_roi.size==0 or re_roi.size==0 or m_roi.size==0:
                continue

            # Predict eye/mouth open vs closed
            le_closed = np.argmax(self.eye_model.predict(self.preprocess_region(le_roi)))==1
            re_closed = np.argmax(self.eye_model.predict(self.preprocess_region(re_roi)))==1
            yawning   = np.argmax(self.mouth_model.predict(self.preprocess_region(m_roi)))==1

            # Count blinks on transition
            blink_now = le_closed and re_closed
            if blink_now and not self._prev_blink_state:
                self.blink_count += 1
            self._prev_blink_state = blink_now

            # Count yawns on transition
            if yawning and not self._prev_yawn_state:
                self.yawn_count += 1
            self._prev_yawn_state = yawning

            # Append state to sequence
            self.state_sequence.append([int(le_closed), int(re_closed), int(yawning)])

            # When buffer full, run LSTM
            if len(self.state_sequence)==self.sequence_length:
                seq = np.expand_dims(np.array(self.state_sequence), axis=0)  # (1,30,3)
                pred = self.lstm_model.predict(seq)
                if np.argmax(pred, axis=1)[0]==1:
                    self.drowsy = True
                    cv2.putText(frame, "Drowsy!", (10,30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # Draw rectangles
            for bb in (le_bb, re_bb, m_bb):
                cv2.rectangle(frame, (bb[0],bb[1]), (bb[2],bb[3]), (0,255,0), 2)

        return self.drowsy, frame
