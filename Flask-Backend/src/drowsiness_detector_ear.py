

# import os
# import cv2
# import dlib
# import numpy as np
# from scipy.spatial import distance as dist

# class DrowsinessDetectorEAR:
#     def __init__(self,
#                  predictor_path="models/shape_predictor_68_face_landmarks.dat",
#                  ear_threshold=0.25,
#                  consec_frames=10):
#         """
#         :param predictor_path: path to dlib’s 68-landmark model
#         :param ear_threshold: below this EAR, the eye is considered closed
#         :param consec_frames: number of consecutive frames of closed eyes to flag drowsy
#         """
#         # Load dlib’s face detector and facial landmark predictor
#         if not os.path.exists(predictor_path):
#             raise FileNotFoundError(f"Missing landmark file: {predictor_path}")
#         self.detector  = dlib.get_frontal_face_detector()
#         self.predictor = dlib.shape_predictor(predictor_path)
        
#         # EAR parameters
#         self.ear_threshold    = ear_threshold
#         self.consec_frames    = consec_frames
#         self.closed_frame_cnt = 0
#         self.drowsy           = False

#     @staticmethod
#     def eye_aspect_ratio(eye):
#         """Compute the EAR for one eye given 6 (x,y) landmark points."""
#         A = dist.euclidean(eye[1], eye[5])
#         B = dist.euclidean(eye[2], eye[4])
#         C = dist.euclidean(eye[0], eye[3])
#         return (A + B) / (2.0 * C)

#     def get_landmarks(self, gray, face):
#         """Return list of (x,y) for each of the 68 landmarks."""
#         shape = self.predictor(gray, face)
#         return [(shape.part(i).x, shape.part(i).y) for i in range(68)]

#     def detect(self, frame):
#         """
#         Process one frame and return (drowsy:bool, annotated_frame:ndarray).
#         Draws EAR and bounding boxes onto the frame.
#         """
#         gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = self.detector(gray)
        
#         # Default: not drowsy
#         self.drowsy = False

#         for face in faces:
#             lm = self.get_landmarks(gray, face)
#             # Extract left/right eye landmarks
#             left_eye  = lm[36:42]
#             right_eye = lm[42:48]
            
#             # Compute EAR for both eyes
#             ear_left  = self.eye_aspect_ratio(left_eye)
#             ear_right = self.eye_aspect_ratio(right_eye)
#             ear       = (ear_left + ear_right) / 2.0
            
#             # Draw the eye contours and EAR value
#             for eye_pts in (left_eye, right_eye):
#                 pts = np.array(eye_pts, dtype=np.int32)
#                 cv2.polylines(frame, [pts], True, (0,255,0), 1)
#             cv2.putText(frame, f"EAR: {ear:.2f}", (face.left(), face.top()-10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
            
#             # Check if EAR is below threshold
#             if ear < self.ear_threshold:
#                 self.closed_frame_cnt += 1
#             else:
#                 # Reset count if eyes open
#                 self.closed_frame_cnt = 0

#             # If eyes have been closed for too long, flag drowsy
#             if self.closed_frame_cnt >= self.consec_frames:
#                 self.drowsy = True
#                 cv2.putText(frame, "DROWSY!", (face.left(), face.bottom()+20),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

#             # Draw face bounding box
#             x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
#             cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), 2)

#         return self.drowsy, frame

import os
import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
import time

class DrowsinessDetectorEAR:
    def __init__(self,
                 predictor_path="models/shape_predictor_68_face_landmarks.dat",
                 ear_threshold=0.25,
                 ear_consec_frames=10,
                 mar_threshold=0.75,
                 mar_consec_frames=15,
                 cooldown_secs=2.0):
        if not os.path.exists(predictor_path):
            raise FileNotFoundError(f"Missing landmark file: {predictor_path}")

        # dlib models
        self.detector  = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)

        # EAR params
        self.ear_threshold     = ear_threshold
        self.ear_consec_frames = ear_consec_frames
        self.eye_closed_cnt    = 0

        # MAR params
        self.mar_threshold      = mar_threshold
        self.mar_consec_frames  = mar_consec_frames
        self.yawn_open_cnt      = 0

        # state
        self.drowsy              = False
        self._last_drowsy_time   = 0
        self.cooldown_secs       = cooldown_secs

    @staticmethod
    def eye_aspect_ratio(eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        return (A + B) / (2.0 * C)

    @staticmethod
    def mouth_aspect_ratio(mouth):
        A = dist.euclidean(mouth[13], mouth[19])
        B = dist.euclidean(mouth[14], mouth[18])
        C = dist.euclidean(mouth[12], mouth[16])
        return (A + B) / (2.0 * C)

    def get_landmarks(self, gray, face):
        shape = self.predictor(gray, face)
        return [(shape.part(i).x, shape.part(i).y) for i in range(68)]

    def detect(self, frame):
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        now   = time.time()
        self.drowsy = False

        for face in faces:
            lm = self.get_landmarks(gray, face)

            # Eyes
            left_eye  = lm[36:42]
            right_eye = lm[42:48]
            ear_left  = self.eye_aspect_ratio(left_eye)
            ear_right = self.eye_aspect_ratio(right_eye)
            ear        = (ear_left + ear_right) / 2.0

            # Mouth
            mouth      = lm[48:68]
            mar        = self.mouth_aspect_ratio(mouth)

            # Debug print
            print(f"DEBUG EAR={ear:.2f} (thr={self.ear_threshold}), MAR={mar:.2f} (thr={self.mar_threshold})")

            # Draw contours
            for pts in (left_eye, right_eye, mouth):
                cv2.polylines(frame, [np.array(pts)], True,
                              (0,255,0) if pts in (left_eye, right_eye) else (0,128,255), 1)

            # Annotate
            cv2.putText(frame, f"EAR:{ear:.2f}", (face.left(), face.top()-30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
            cv2.putText(frame, f"MAR:{mar:.2f}", (face.left(), face.top()-15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

            # Eye logic
            if ear < self.ear_threshold:
                self.eye_closed_cnt += 1
            else:
                self.eye_closed_cnt = 0

            # Yawn logic
            if mar > self.mar_threshold:
                self.yawn_open_cnt += 1
            else:
                self.yawn_open_cnt = 0

            # Check cooldown
            # if now - self._last_drowsy_time < self.cooldown_secs:
            #     # still in cooldown → skip detection
            #     continue

            # If either criterion met
            if (self.eye_closed_cnt  >= self.ear_consec_frames or
                self.yawn_open_cnt   >= self.mar_consec_frames):
                print("Yawn Count :", self.yawn_open_cnt)
                self.drowsy = True
                self._last_drowsy_time = now
                # annotate
                cv2.putText(frame, "!!! DROWSY !!!", (face.left(), face.bottom()+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
                # reset counters so you can detect again after cooldown
                self.eye_closed_cnt = 0
                self.yawn_open_cnt = 0

            # Face box
            x1,y1,x2,y2 = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(frame, (x1,y1),(x2,y2), (255,0,0), 2)

            

        return self.drowsy, frame
