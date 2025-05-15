# import os
# import cv2
# import dlib
# import numpy as np
# import time
# from tensorflow.keras.models import load_model

# class DrowsinessDetector:
#     def __init__(self):
        
#         self.detector = dlib.get_frontal_face_detector()
        
#         # Get the directory path of this file
#         base_dir = os.path.dirname(os.path.abspath(__file__))

#         # Construct absolute path to the model file
#         predictor_path = os.path.join(base_dir, "..", "models", "shape_predictor_68_face_landmarks.dat")

#         self.predictor = dlib.shape_predictor(predictor_path)

#         base_dir = os.path.dirname(os.path.abspath(__file__))
#         eye_model_path = os.path.join(base_dir, "..", "models", "eye_model.h5")

#         self.eye_model = load_model(eye_model_path)

#         mouth_model_path = os.path.join(base_dir, "..", "models", "mouth_model.h5")
#         self.mouth_model = load_model(mouth_model_path) 
        
#         # Blink detection parameters
#         self.blink_start_time = None
#         self.blink_duration_threshold = 0.6  # in seconds
#         self.blink_count = 0
#         self.blink_threshold_count = 3  # blinks to trigger drowsiness

#         # Yawning detection parameters
#         self.yawn_count = 0
#         self.yawn_threshold_count = 5  # yawns to trigger drowsiness
#         self.last_yawn_time = time.time()  # Time when the last yawn was counted

#         self.img_size = (64, 64)

#     def preprocess_region(self, region):
#         region = cv2.resize(region, self.img_size)
#         region = region / 255.0
#         return np.expand_dims(region, axis=0)

#     def get_bounding_box(self, points, frame):
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

#             left_eye_pred = self.eye_model.predict(self.preprocess_region(left_eye_region))
#             right_eye_pred = self.eye_model.predict(self.preprocess_region(right_eye_region))
#             mouth_pred = self.mouth_model.predict(self.preprocess_region(mouth_region))

#             left_eye_closed = np.argmax(left_eye_pred) == 1
#             right_eye_closed = np.argmax(right_eye_pred) == 1
#             is_yawning = np.argmax(mouth_pred) == 1

#             # ----- Blink Detection -----
#             if left_eye_closed and right_eye_closed:
#                 if self.blink_start_time is None:
#                     self.blink_start_time = time.time()
#                 else:
#                     blink_duration = time.time() - self.blink_start_time
#                     if blink_duration >= self.blink_duration_threshold:
#                         self.blink_count += 1
#                         print(f"[Blink] Duration: {blink_duration:.2f}s, Count: {self.blink_count}")
#                         self.blink_start_time = None
            
#             else:
#                 self.blink_start_time = None

#             if self.blink_count >= self.blink_threshold_count:
#                 drowsy = True
#                 print("Drowsiness Detected: Prolonged blinking.")
#                 cv2.putText(frame, "Drowsy!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#                 self.blink_count = 0  # Reset blink count after detection

#             # ----- Yawning Detection -----
#             current_time = time.time()
#             if is_yawning:
#                 # Ensure the mouth region is valid and the prediction is reliable
#                 if mouth_region.size > 0:
#                     print(f"[Debug] Mouth prediction: {mouth_pred}, Is yawning: {is_yawning}")
#                     # Start timing the yawn if not already started
#                     if self.last_yawn_time is None:
#                         self.last_yawn_time = current_time
#                     else:
#                         yawn_duration = current_time - self.last_yawn_time
#                         if yawn_duration >= 4:  # Yawning for 5 seconds
#                             drowsy = True
#                             print("Drowsiness Detected: Prolonged yawning.")
#                             cv2.putText(frame, "Drowsy!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#                             self.last_yawn_time = None  # Reset yawn timer after detection
#                             return drowsy, frame
#                 else:
#                     print("[Warning] Invalid mouth region detected.")
#             else:
#                 # Reset the yawn timer if no yawning is detected
#                 self.last_yawn_time = None

#             # ----- Draw Rectangles -----
#             cv2.rectangle(frame, (left_eye_coords[0], left_eye_coords[1]),
#                           (left_eye_coords[2], left_eye_coords[3]), (0, 255, 0), 2)
#             cv2.rectangle(frame, (right_eye_coords[0], right_eye_coords[1]),
#                           (right_eye_coords[2], right_eye_coords[3]), (0, 255, 0), 2)
#             cv2.rectangle(frame, (mouth_coords[0], mouth_coords[1]),
#                           (mouth_coords[2], mouth_coords[3]), (0, 255, 0), 2)

#         return drowsy, frame

# import os
# import cv2
# import dlib
# import numpy as np
# import time
# from tensorflow.keras.models import load_model

# class DrowsinessDetector:
#     def __init__(self):
#         # Get the directory path of this file
#         base_dir = os.path.dirname(os.path.abspath(__file__))

#         # Construct absolute paths to model files
#         predictor_path = os.path.join(base_dir, "..", "models", "shape_predictor_68_face_landmarks.dat")
#         eye_model_path = os.path.join(base_dir, "..", "models", "eye_model.h5")
#         mouth_model_path = os.path.join(base_dir, "..", "models", "mouth_model.h5")

#         # Check if model files exist
#         if not os.path.exists(predictor_path):
#             raise FileNotFoundError(f"Shape predictor file not found at {predictor_path}")
#         if not os.path.exists(eye_model_path):
#             raise FileNotFoundError(f"Eye model file not found at {eye_model_path}")
#         if not os.path.exists(mouth_model_path):
#             raise FileNotFoundError(f"Mouth model file not found at {mouth_model_path}")

#         # Initialize face detector and landmark predictor
#         self.detector = dlib.get_frontal_face_detector()
#         self.predictor = dlib.shape_predictor(predictor_path)

#         # Load eye and mouth models
#         self.eye_model = load_model(eye_model_path)
#         self.mouth_model = load_model(mouth_model_path)

#         # Blink detection parameters
#         self.blink_start_time = None
#         self.blink_duration_threshold = 0.6  # in seconds
#         self.blink_count = 0
#         self.blink_threshold_count = 3  # blinks to trigger drowsiness

#         # Yawning detection parameters
#         self.yawn_count = 0
#         self.yawn_threshold_count = 5  # yawns to trigger drowsiness
#         self.last_yawn_time = None  # Time when the last yawn was detected

#         # Image size for model input
#         self.img_size = (64, 64)

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
#         """Detect drowsiness in the frame and return the status and processed frame."""
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = self.detector(gray)

#         if len(faces) == 0:
#             return False, frame

#         drowsy = False

#         for face in faces:
#             landmarks = self.predictor(gray, face)

#             # Extract eye and mouth landmarks
#             left_eye_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)]
#             right_eye_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)]
#             mouth_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)]

#             # Get bounding boxes for eyes and mouth
#             left_eye_coords = self.get_bounding_box(left_eye_pts, frame)
#             right_eye_coords = self.get_bounding_box(right_eye_pts, frame)
#             mouth_coords = self.get_bounding_box(mouth_pts, frame)

#             # Extract regions from the frame
#             left_eye_region = frame[left_eye_coords[1]:left_eye_coords[3], left_eye_coords[0]:left_eye_coords[2]]
#             right_eye_region = frame[right_eye_coords[1]:right_eye_coords[3], right_eye_coords[0]:right_eye_coords[2]]
#             mouth_region = frame[mouth_coords[1]:mouth_coords[3], mouth_coords[0]:mouth_coords[2]]

#             # Skip if any region is empty
#             if left_eye_region.size == 0 or right_eye_region.size == 0 or mouth_region.size == 0:
import os
import cv2
import dlib
import numpy as np
import time
from tensorflow.keras.models import load_model
# from voice_assistant import VoiceAssistant

# voice = VoiceAssistant()

class DrowsinessDetector:
    def __init__(self):
        # Get the directory path of this file
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct absolute paths to model files
        predictor_path = os.path.join(base_dir, "models", "shape_predictor_68_face_landmarks.dat")
        eye_model_path = os.path.join(base_dir, "models", "eye_model.h5")
        mouth_model_path = os.path.join(base_dir, "models", "mouth_model.h5")

        # Check if model files exist
        if not os.path.exists(predictor_path):
            raise FileNotFoundError(f"Shape predictor file not found at {predictor_path}")
        if not os.path.exists(eye_model_path):
            raise FileNotFoundError(f"Eye model file not found at {eye_model_path}")
        if not os.path.exists(mouth_model_path):
            raise FileNotFoundError(f"Mouth model file not found at {mouth_model_path}")

        # Initialize face detector and landmark predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)

        # Load eye and mouth models
        self.eye_model = load_model(eye_model_path)
        self.mouth_model = load_model(mouth_model_path)

        # Blink detection parameters
        self.blink_start_time = None
        self.blink_duration_threshold = 0.6  # in seconds
        self.blink_count = 0
        self.blink_threshold_count = 3  # blinks to trigger drowsiness

        # Yawning detection parameters
        self.yawn_count = 0
        self.yawn_threshold_count = 3  # yawns to trigger drowsiness
        self.last_yawn_time = None  # Time when the last yawn was detected

        # Drowsy state persistence
        self.drowsy_end_time = 0  # Time when drowsy state ends
        self.drowsy_duration = 5  # Seconds to keep drowsy state after detection

        # Image size for model input
        self.img_size = (64, 64)

    def reset(self):
        """Reset detection state."""
        self.blink_start_time = None
        self.blink_count = 0
        self.yawn_count = 0
        self.last_yawn_time = None
        self.drowsy_end_time = 0



    def preprocess_region(self, region):
        """Preprocess the region for model input."""
        region = cv2.resize(region, self.img_size)
        region = region / 255.0
        return np.expand_dims(region, axis=0)

    def get_bounding_box(self, points, frame):
        """Get bounding box for the given points with padding."""
        x_coords, y_coords = zip(*points)
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        padding = 10
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(frame.shape[1], x_max + padding)
        y_max = min(frame.shape[0], y_max + padding)
        return (x_min, y_min, x_max, y_max)

    def detect_drowsiness(self, frame):
        """Detect drowsiness and return status and annotated frame."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        if len(faces) == 0:
            return False, frame

        current_time = time.time()

        for face in faces:
            landmarks = self.predictor(gray, face)

            left_eye_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)]
            right_eye_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)]
            mouth_pts = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)]

            left_eye_coords = self.get_bounding_box(left_eye_pts, frame)
            right_eye_coords = self.get_bounding_box(right_eye_pts, frame)
            mouth_coords = self.get_bounding_box(mouth_pts, frame)

            left_eye_region = frame[left_eye_coords[1]:left_eye_coords[3], left_eye_coords[0]:left_eye_coords[2]]
            right_eye_region = frame[right_eye_coords[1]:right_eye_coords[3], right_eye_coords[0]:right_eye_coords[2]]
            mouth_region = frame[mouth_coords[1]:mouth_coords[3], mouth_coords[0]:mouth_coords[2]]

            if left_eye_region.size == 0 or right_eye_region.size == 0 or mouth_region.size == 0:
                continue

            left_eye_input = self.preprocess_region(left_eye_region)
            right_eye_input = self.preprocess_region(right_eye_region)
            mouth_input = self.preprocess_region(mouth_region)

            left_eye_pred = self.eye_model.predict(left_eye_input)
            right_eye_pred = self.eye_model.predict(right_eye_input)
            mouth_pred = self.mouth_model.predict(mouth_input)

            left_eye_closed = np.argmax(left_eye_pred) == 1
            right_eye_closed = np.argmax(right_eye_pred) == 1
            is_yawning = np.argmax(mouth_pred) == 1

            # Blink Detection
            if left_eye_closed and right_eye_closed:
                if self.blink_start_time is None:
                    self.blink_start_time = current_time
                else:
                    blink_duration = current_time - self.blink_start_time
                    if blink_duration >= self.blink_duration_threshold:
                        self.blink_count += 1
                        print(f"[Blink] Duration: {blink_duration:.2f}s, Count: {self.blink_count}")
                        self.blink_start_time = None
            else:
                self.blink_start_time = None

            # Yawn Detection
            if is_yawning and mouth_region.size > 0:
                if self.last_yawn_time is None:
                    self.last_yawn_time = current_time
                else:
                    yawn_duration = current_time - self.last_yawn_time
                    if yawn_duration >= 2:
                        self.yawn_count += 1
                        print(f"[Yawn] Duration: {yawn_duration:.2f}s, Count: {self.yawn_count}")
                        self.last_yawn_time = None
            else:
                self.last_yawn_time = None

            # Check if thresholds are met
            if self.blink_count >= self.blink_threshold_count or self.yawn_count >= self.yawn_threshold_count:
                self.drowsy_end_time = current_time + self.drowsy_duration
                self.blink_count = 0
                self.yawn_count = 0
                print("Drowsiness detected. Setting drowsy state for 5 seconds.")

            # Determine if currently drowsy based on timer
            is_drowsy = current_time < self.drowsy_end_time

            
            # Draw rectangles
            cv2.rectangle(frame, (left_eye_coords[0], left_eye_coords[1]),
                          (left_eye_coords[2], left_eye_coords[3]), (0, 255, 0), 2)
            cv2.rectangle(frame, (right_eye_coords[0], right_eye_coords[1]),
                          (right_eye_coords[2], right_eye_coords[3]), (0, 255, 0), 2)
            cv2.rectangle(frame, (mouth_coords[0], mouth_coords[1]),
                          (mouth_coords[2], mouth_coords[3]), (0, 255, 0), 2)

        return is_drowsy, frame