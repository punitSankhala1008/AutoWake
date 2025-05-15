# # from flask import Flask, Response, jsonify, request
# # import cv2
# # import time
# # from src.drowsiness_detector import DrowsinessDetector
# # from src.drowsiness_detector_lstm import DrowsinessDetectorLSTM
# # from src.voice_assistant import VoiceAssistant

# # app = Flask(__name__)

# # # Initialize detectors and voice assistant
# # cnn_detector = DrowsinessDetector()
# # lstm_detector = DrowsinessDetectorLSTM()
# # voice = VoiceAssistant()

# # # Global variables
# # video_capture = cv2.VideoCapture(0)
# # if not video_capture.isOpened():
# #     raise RuntimeError("Error: Could not open webcam.")

# # drowsy_state = {
# #     "drowsy": False,
# #     "blink_count": 0,
# #     "yawn_count": 0,
# #     "selected_model": "cnn"
# # }
# # last_alert_time = 0
# # alert_interval = 5  # Seconds between alerts

# # def generate_frames():
# #     """Generate annotated frames for streaming."""
# #     global last_alert_time
# #     target_fps = 30
# #     frame_delay = 1 / target_fps  # Delay in seconds

# #     while True:
# #         success, frame = video_capture.read()
# #         if not success:
# #             print("Error: Could not read frame.")
# #             break

# #         # Detect drowsiness based on selected model
# #         if drowsy_state["selected_model"] == "cnn":
# #             is_drowsy, processed_frame = cnn_detector.detect_drowsiness(frame)
# #             drowsy_state["blink_count"] = cnn_detector.blink_count
# #             drowsy_state["yawn_count"] = cnn_detector.yawn_count
# #         else:
# #             is_drowsy, processed_frame = lstm_detector.detect_drowsiness(frame)
# #             drowsy_state["blink_count"] = lstm_detector.blink_count
# #             drowsy_state["yawn_count"] = lstm_detector.yawn_count

# #         drowsy_state["drowsy"] = is_drowsy
# #         print(f"Drowsy: {is_drowsy}")
# #         # Trigger voice alert
# #         current_time = time.time()
# #         if is_drowsy :
# #             voice.speak("Warning: You appear to be drowsy. Please stay alert!")
            

# #         # Encode frame as JPEG
# #         ret, buffer = cv2.imencode('.jpg', processed_frame)
# #         if not ret:
# #             continue
# #         frame_bytes = buffer.tobytes()

# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# #         time.sleep(frame_delay)

# # @app.route('/video')
# # def video_feed():
# #     """Stream the processed video feed."""
# #     return Response(generate_frames(),
# #                     mimetype='multipart/x-mixed-replace; boundary=frame')

# # @app.route('/status')
# # def get_status():
# #     """Return drowsiness status."""
# #     if drowsy_state["drowsy"]:
# #         voice.speak("Warning: You appear to be drowsy. Please stay alert!")
            
# #     return jsonify(drowsy_state)

# # @app.route('/select_model', methods=['POST'])
# # def select_model():
# #     """Handle model selection."""
# #     model = request.json.get('models')
# #     print(f"Selected model: {model}")
# #     if model in ['lstm_model.h5']:
        
# #         drowsy_state["selected_model"] = model
# #         # Reset detectors to clear state
# #         cnn_detector.reset()
# #         lstm_detector.reset()
# #         return jsonify({"status": "success", "model": model})
# #     return jsonify({"status": "error", "message": "Invalid model"}), 400

# # def cleanup():
# #     """Release resources."""
# #     video_capture.release()

# # if __name__ == '__main__':
# #     try:
# #         app.run(host='localhost', port=5000, threaded=True)
# #     finally:
# #         cleanup()

# # from flask import Flask, Response, jsonify, request
# # from flask_cors import CORS
# # import cv2, time
# # from src.drowsiness_detector import DrowsinessDetector
# # from src.drowsiness_detector_lstm import DrowsinessDetectorLSTM
# # from src.voice_assistant import VoiceAssistant

# # app = Flask(__name__)
# # CORS(app)

# # # Initialize detectors and voice assistant
# # cnn_detector = DrowsinessDetector()
# # lstm_detector = DrowsinessDetectorLSTM()
# # voice = VoiceAssistant()

# # # Global variables
# # video_capture = cv2.VideoCapture(0)
# # if not video_capture.isOpened():
# #     raise RuntimeError("Error: Could not open webcam.")

# # drowsy_state = {
# #     "drowsy": False,
# #     "blink_count": 0,
# #     "yawn_count": 0,
# #     "selected_model": "cnn"
# # }
# # last_alert_time = 0
# # alert_interval = 5  # Seconds between alerts

# # def generate_frames():
# #     """Generate annotated frames for streaming."""
# #     global last_alert_time
# #     target_fps = 30
# #     frame_delay = 1 / target_fps  # Delay in seconds

# #     while True:
# #         success, frame = video_capture.read()
# #         if not success:
# #             print("Error: Could not read frame.")
# #             break

# #         current_time = time.time()

# #         # Detect drowsiness based on selected model
# #         try:
# #             if drowsy_state["selected_model"] == "cnn":
# #                 is_drowsy, processed_frame = cnn_detector.detect_drowsiness(frame)
# #                 drowsy_state["blink_count"] = cnn_detector.blink_count
# #                 drowsy_state["yawn_count"] = cnn_detector.yawn_count
# #             else:
# #                 is_drowsy, processed_frame = lstm_detector.detect_drowsiness(frame)
# #                 drowsy_state["blink_count"] = lstm_detector.blink_count
# #                 drowsy_state["yawn_count"] = lstm_detector.yawn_count
# #         except Exception as e:
# #             print(f"Error in drowsiness detection: {e}")
# #             continue

# #         drowsy_state["drowsy"] = is_drowsy
# #         print(f"Drowsy: {is_drowsy}")

# #         # Trigger voice alert with interval check
# #         if is_drowsy and (current_time - last_alert_time >= alert_interval):
# #             voice.speak("Warning: You appear to be drowsy. Please stay alert!")
# #             last_alert_time = current_time

# #         # Encode frame as JPEG
# #         try:
# #             ret, buffer = cv2.imencode('.jpg', processed_frame)
# #             if not ret:
# #                 print("Error: Could not encode frame.")
# #                 continue
# #             frame_bytes = buffer.tobytes()
# #         except Exception as e:
# #             print(f"Error encoding frame: {e}")
# #             continue

# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# #         time.sleep(frame_delay)

# # @app.route('/video')
# # def video_feed():
# #     """Stream the processed video feed."""
# #     return Response(generate_frames(),
# #                     mimetype='multipart/x-mixed-replace; boundary=frame')

# # @app.route('/status')
# # def get_status():
# #     """Return drowsiness status without triggering voice alert."""
# #     return jsonify(drowsy_state)

# # # @app.route('/select_model', methods=['POST'])
# # # def select_model():
# # #     """Handle model selection."""
# # #     model = request.json.get('model')
# # #     print(f"Selected model: {model}")
# # #     if model in ['cnn', 'lstm']:
# # #         drowsy_state["selected_model"] = model
# # #         # Reset detectors to clear state
# # #         cnn_detector.reset()
# # #         lstm_detector.reset()
# # #         return jsonify({"status": "success", "model": model})
# # #     return jsonify({"status": "error", "message": "Invalid model"}), 400

# # @app.route('/select_model', methods=['POST'])
# # def select_model():
# #     model = request.json.get('model')
# #     if model in ['cnn', 'lstm']:
# #         drowsy_state["selected_model"] = model
# #         cnn_detector.reset()
# #         lstm_detector.reset()
# #         return jsonify({"status": "success", "model": model})
# #     return jsonify({"status": "error", "message": "Invalid model"}), 400


# # def cleanup():
# #     """Release resources."""
# #     try:
# #         voice.stop()
# #     except Exception as e:
# #         print(f"Error stopping VoiceAssistant: {e}")
# #     try:
# #         video_capture.release()
# #     except Exception as e:
# #         print(f"Error releasing video capture: {e}")

# # if __name__ == '__main__':
# #     try:
# #         app.run(host='localhost', port=5000, threaded=True)
# #     except KeyboardInterrupt:
# #         print("Shutting down Flask server...")
# #     finally:
# #         cleanup()
        

# # New Code

# # Flask-Backend/server.py

# # import os
# # import sys
# # import time
# # import cv2
# # from flask import Flask, Response, jsonify, request
# # from flask_cors import CORS

# # # 1) Make sure 'src' is on the import path
# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # SRC_DIR  = os.path.join(BASE_DIR, 'src')
# # if SRC_DIR not in sys.path:
# #     sys.path.insert(0, SRC_DIR)

# # # Now import your detectors & voice assistant
# # from drowsiness_detector import DrowsinessDetector
# # from drowsiness_detector_lstm import DrowsinessDetectorLSTM
# # from voice_assistant import VoiceAssistant

# # app = Flask(__name__)
# # CORS(app)  # allow all origins (Electron)

# # # Initialize once
# # cnn_detector = DrowsinessDetector()
# # lstm_detector = DrowsinessDetectorLSTM()
# # voice = VoiceAssistant()

# # # Shared state
# # video_capture = cv2.VideoCapture(0)
# # if not video_capture.isOpened():
# #     raise RuntimeError("Could not open webcam.")

# # drowsy_state = {
# #     "drowsy": False,
# #     "blink_count": 0,
# #     "yawn_count": 0,
# #     "selected_model": "cnn"
# # }
# # last_alert_time = 0
# # ALERT_INTERVAL = 0  # seconds

# # def generate_frames():
# #     global last_alert_time
# #     fps = 30
# #     delay = 1.0 / fps

# #     while True:
# #         try:
# #             success, frame = video_capture.read()
# #             if not success:
# #                 break

# #             now = time.time()
# #             model = drowsy_state["selected_model"]

# #             # pick detector
# #             if model == 'cnn':
# #                 is_d, proc = cnn_detector.detect_drowsiness(frame)
# #                 drowsy_state["blink_count"] = cnn_detector.blink_count
# #                 drowsy_state["yawn_count"] = cnn_detector.yawn_count
# #             else:
# #                 is_d, proc = lstm_detector.detect_drowsiness(frame)
# #                 drowsy_state["blink_count"] = lstm_detector.blink_count
# #                 drowsy_state["yawn_count"] = lstm_detector.yawn_count

# #             drowsy_state["drowsy"] = is_d

# #             # voice alert
# #             if is_d and (now - last_alert_time >= ALERT_INTERVAL):
# #                 voice.speak("Warning: You appear to be drowsy. Please stay alert!")
# #                 last_alert_time = now

# #             # encode frame
# #             ret, buf = cv2.imencode('.jpg', proc)
# #             if not ret:
# #                 continue

# #             frame_bytes = buf.tobytes()
# #             yield (b'--frame\r\n'
# #                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
# #             time.sleep(delay)

# #         except Exception as e:
# #             # log and continue streaming
# #             print("Error in stream:", str(e))
# #             continue

# # @app.route('/')
# # def home():
# #     return jsonify({"status":"ok","message":"Flask backend running"}), 200

# # @app.route('/video')
# # def video_feed():
# #     try:
# #         return Response(generate_frames(),
# #                         mimetype='multipart/x-mixed-replace; boundary=frame')
# #     except Exception as e:
# #         return jsonify({"status":"error","message":str(e)}), 500

# # @app.route('/status')
# # def get_status():
# #     try:
# #         return jsonify(drowsy_state), 200
# #     except Exception as e:
# #         print("Error in /status:", e)
# #         return jsonify({"status":"error","message":str(e)}), 500
    
# # @app.route('/select_model', methods=['POST'])
# # def select_model():
# #     try:
# #         model = request.json.get('model')
# #         if model not in ('cnn','lstm'):
# #             return jsonify({"status":"error","message":"Invalid model"}), 400

# #         drowsy_state["selected_model"] = model
# #         cnn_detector.reset()
# #         lstm_detector.reset()
# #         return jsonify({"status":"success","model":model}), 200

# #     except Exception as e:
# #         return jsonify({"status":"error","message":str(e)}), 500

# # def cleanup():
# #     try:
# #         voice.stop()
# #     except:
# #         pass
# #     try:
# #         video_capture.release()
# #     except:
# #         pass

# # if __name__ == '__main__':
# #     try:
# #         # threaded=True to allow multiple simultaneous requests (video + status/select)
# #         app.run(host='127.0.0.1', port=5000, threaded=True, debug=False)
# #     except KeyboardInterrupt:
# #         pass
# #     finally:
# #         cleanup()


# # from flask import Flask, Response, jsonify, request
# # import cv2
# # import time
# # from src.drowsiness_detector import DrowsinessDetector
# # from src.drowsiness_detector_lstm import DrowsinessDetectorLSTM
# # from src.voice_assistant import VoiceAssistant

# # app = Flask(__name__)

# # # Initialize detectors and voice assistant
# # cnn_detector = DrowsinessDetector()
# # lstm_detector = DrowsinessDetectorLSTM()
# # voice = VoiceAssistant()

# # # Global variables
# # video_capture = cv2.VideoCapture(0)
# # if not video_capture.isOpened():
# #     raise RuntimeError("Error: Could not open webcam.")

# # drowsy_state = {
# #     "drowsy": False,
# #     "blink_count": 0,
# #     "yawn_count": 0,
# #     "selected_model": "cnn"
# # }
# # last_alert_time = 0  # Seconds since last alert
# # alert_interval = 1  # Seconds between alerts
# # previous_drowsy_state = False  # Track previous drowsy state to detect state changes

# # def generate_frames():
# #     """Generate annotated frames for streaming."""
# #     global last_alert_time, previous_drowsy_state
# #     target_fps = 30
# #     frame_delay = 1 / target_fps  # Delay in seconds

# #     while True:
# #         success, frame = video_capture.read()
# #         if not success:
# #             print("Error: Could not read frame.")
# #             break

# #         current_time = time.time()

# #         # Detect drowsiness based on selected model
# #         try:
# #             if drowsy_state["selected_model"] == "cnn":
# #                 is_drowsy, processed_frame = cnn_detector.detect_drowsiness(frame)
# #                 drowsy_state["blink_count"] = cnn_detector.blink_count
# #                 drowsy_state["yawn_count"] = cnn_detector.yawn_count
# #             else:
# #                 is_drowsy, processed_frame = lstm_detector.detect_drowsiness(frame)
# #                 drowsy_state["blink_count"] = lstm_detector.blink_count
# #                 drowsy_state["yawn_count"] = lstm_detector.yawn_count
# #         except Exception as e:
# #             print(f"Error in drowsiness detection: {e}")
# #             continue

# #         drowsy_state["drowsy"] = is_drowsy
# #         print(f"Drowsy: {is_drowsy}")

# #         # Check if state changed from alert to drowsy
# #         state_changed = is_drowsy and not previous_drowsy_state
# #         time_elapsed = current_time - last_alert_time >= alert_interval
        
# #         # Trigger voice alert when:
# #         # 1. State changes from alert to drowsy OR
# #         # 2. Person remains drowsy and alert interval has passed
# #         if is_drowsy and (state_changed or time_elapsed):
# #             print(f"Triggering alert: state_changed={state_changed}, time_elapsed={time_elapsed}")
# #             voice.speak("Warning: You appear to be drowsy. Please stay alert!")
# #             last_alert_time = current_time
        
# #         # Update previous state
# #         previous_drowsy_state = is_drowsy

# #         # Encode frame as JPEG
# #         try:
# #             ret, buffer = cv2.imencode('.jpg', processed_frame)
# #             if not ret:
# #                 print("Error: Could not encode frame.")
# #                 continue
# #             frame_bytes = buffer.tobytes()
# #         except Exception as e:
# #             print(f"Error encoding frame: {e}")
# #             continue

# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# #         time.sleep(frame_delay)

# # @app.route('/video')
# # def video_feed():
# #     """Stream the processed video feed."""
# #     return Response(generate_frames(),
# #                     mimetype='multipart/x-mixed-replace; boundary=frame')

# # @app.route('/status')
# # def get_status():
# #     """Return drowsiness status without triggering voice alert."""
# #     return jsonify(drowsy_state)

# # @app.route('/select_model', methods=['POST'])
# # def select_model():
# #     """Handle model selection."""
# #     model = request.json.get('model')
# #     print(f"Selected model: {model}")
# #     if model in ['cnn', 'lstm']:
# #         drowsy_state["selected_model"] = model
# #         # Reset detectors to clear state
# #         cnn_detector.reset()
# #         lstm_detector.reset()
# #         return jsonify({"status": "success", "model": model})
# #     return jsonify({"status": "error", "message": "Invalid model"}), 400

# # def cleanup():
# #     """Release resources."""
# #     try:
# #         voice.stop()
# #     except Exception as e:
# #         print(f"Error stopping VoiceAssistant: {e}")
# #     try:
# #         video_capture.release()
# #     except Exception as e:
# #         print(f"Error releasing video capture: {e}")

# # if __name__ == '__main__':
# #     try:
# #         app.run(host='localhost', port=5000, threaded=True)
# #     except KeyboardInterrupt:
# #         print("Shutting down Flask server...")
# #     finally:
# #         cleanup()

# from flask import Flask, Response, jsonify, request
# import cv2
# import time
# import threading
# import pyttsx3
# import queue
# from src.drowsiness_detector import DrowsinessDetector
# from src.drowsiness_detector_lstm import DrowsinessDetectorLSTM
# from src.voice_assistant import VoiceAssistant

# app = Flask(__name__)

# # Initialize detectors and voice assistant
# cnn_detector = DrowsinessDetector()
# lstm_detector = DrowsinessDetectorLSTM()
# voice = VoiceAssistant()

# engine = pyttsx3.init()
# engine.setProperty('rate', 150)  # Set the speed of speech
# engine.setProperty('volume', 1)

# # Global variables with thread lock
# import threading
# drowsy_state_lock = threading.Lock()
# drowsy_state = {
#     "drowsy": False,
#     "blink_count": 0,
#     "yawn_count": 0,
#     "selected_model": "cnn"
# }

# # Shared frame queue for producer-consumer pattern
# frame_queue = queue.Queue(maxsize=5)  # Limit queue size
# last_alert_time = 0
# alert_interval = 1
# previous_drowsy_state = False

# # Flag to signal thread termination
# shutdown_event = threading.Event()

# def capture_frames():
#     """Capture frames from camera in a separate thread."""
#     video_capture = cv2.VideoCapture(0)
#     if not video_capture.isOpened():
#         print("Error: Could not open webcam.")
#         return

#     try:
#         while not shutdown_event.is_set():
#             success, frame = video_capture.read()
#             if not success:
#                 print("Error: Could not read frame.")
#                 time.sleep(0.1)  # Small delay before retry
#                 continue
                
#             # If queue is full, remove oldest item
#             if frame_queue.full():
#                 try:
#                     frame_queue.get_nowait()
#                 except queue.Empty:
#                     pass
                    
#             frame_queue.put(frame)
#             time.sleep(0.01)  # Slight delay to prevent CPU overuse
#     finally:
#         video_capture.release()
#         print("Camera released")

# def generate_frames():
#     """Process frames and generate output stream."""
#     global last_alert_time, previous_drowsy_state
    
#     while not shutdown_event.is_set():
#         try:
#             # Get frame with timeout to allow thread to exit when shutdown
#             frame = frame_queue.get(timeout=1.0)
#             current_time = time.time()
            
#             # Select model and detect drowsiness
#             with drowsy_state_lock:
#                 selected_model = drowsy_state["selected_model"]
            
#             # Detect drowsiness based on selected model
#             try:
#                 if selected_model == "cnn":
#                     is_drowsy, processed_frame = cnn_detector.detect_drowsiness(frame.copy())
#                     with drowsy_state_lock:
#                         drowsy_state["blink_count"] = cnn_detector.blink_count
#                         drowsy_state["yawn_count"] = cnn_detector.yawn_count
#                 else:
#                     is_drowsy, processed_frame = lstm_detector.detect_drowsiness(frame.copy())
#                     with drowsy_state_lock:
#                         drowsy_state["blink_count"] = lstm_detector.blink_count
#                         drowsy_state["yawn_count"] = lstm_detector.yawn_count
#             except Exception as e:
#                 print(f"Error in drowsiness detection: {e}")
#                 continue
                
#             # Update drowsy state with lock
#             with drowsy_state_lock:
#                 drowsy_state["drowsy"] = is_drowsy
#                 local_prev_drowsy = previous_drowsy_state
#                 previous_drowsy_state = is_drowsy
            
#             # Generate alert if needed
#             state_changed = is_drowsy and not local_prev_drowsy
#             time_elapsed = current_time - last_alert_time >= alert_interval
            
#             if is_drowsy and (state_changed or time_elapsed):
#                 print(f"Triggering alert: state_changed={state_changed}, time_elapsed={time_elapsed}")
#                 voice.speak("Warning: You appear to be drowsy. Please stay alert!")
#                 voice.speech_thread.join()  # Wait for the speech thread to finish
#                 last_alert_time = current_time
                
#             # Add status text on frame
#             status_text = f"Status: {'DROWSY' if is_drowsy else 'ALERT'}"
#             cv2.putText(processed_frame, status_text, (10, 30), 
#                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if is_drowsy else (0, 255, 0), 2)
                
#             # Encode frame
#             ret, buffer = cv2.imencode('.jpg', processed_frame)
#             if not ret:
#                 continue
                
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
#         except queue.Empty:
#             # Just continue if no frame is available
#             continue
#         except Exception as e:
#             print(f"Error processing frame: {e}")
#             time.sleep(0.1)  # Add delay to prevent rapid error looping

# @app.route('/video')
# def video_feed():
#     """Stream the processed video feed."""
#     return Response(generate_frames(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/status')
# def get_status():
#     """Return drowsiness status."""
#     with drowsy_state_lock:
#         current_state = drowsy_state.copy()
#     return jsonify(current_state)

# @app.route('/select_model', methods=['POST'])
# def select_model():
#     """Handle model selection."""
#     model = request.json.get('model')
#     if model in ['cnn', 'lstm']:
#         with drowsy_state_lock:
#             drowsy_state["selected_model"] = model
#         # Reset detectors
#         cnn_detector.reset()
#         lstm_detector.reset()
#         return jsonify({"status": "success", "model": model})
#     return jsonify({"status": "error", "message": "Invalid model"}), 400

# def cleanup():
#     """Release resources properly."""
#     print("Starting cleanup...")
#     shutdown_event.set()  # Signal threads to terminate
#     try:
#         voice.stop()
#     except Exception as e:
#         print(f"Error stopping VoiceAssistant: {e}")

# if __name__ == '__main__':
#     # Start frame capture thread
#     capture_thread = threading.Thread(target=capture_frames)
#     capture_thread.daemon = True
#     capture_thread.start()
    
#     try:
#         app.run(host='localhost', port=5000, threaded=True)
#     except KeyboardInterrupt:
#         print("Shutting down Flask server...")
#     finally:
#         cleanup()
#         # Give threads time to clean up
#         time.sleep(1)

# from flask import Flask, Response, jsonify, request
# import cv2
# import time
# import threading
# import queue
# from src.drowsiness_detector import DrowsinessDetector
# from src.drowsiness_detector_lstm import DrowsinessDetectorLSTM
# from src.voice_assistant import VoiceAssistant

# app = Flask(__name__)

# # Initialize detectors and voice assistant
# cnn_detector = DrowsinessDetector()
# lstm_detector = DrowsinessDetectorLSTM()
# voice = VoiceAssistant()

# # Global variables with thread lock
# import threading
# drowsy_state_lock = threading.Lock()
# drowsy_state = {
#     "drowsy": False,
#     "blink_count": 0,
#     "yawn_count": 0,
#     "selected_model": "cnn"
# }

# # Shared frame queue for producer-consumer pattern
# frame_queue = queue.Queue(maxsize=5)  # Limit queue size
# last_alert_time = 0
# alert_interval = 1
# previous_drowsy_state = False

# # Flag to signal thread termination
# shutdown_event = threading.Event()

# def capture_frames():
#     """Capture frames from camera in a separate thread."""
#     video_capture = cv2.VideoCapture(0)
#     if not video_capture.isOpened():
#         print("Error: Could not open webcam.")
#         return

#     try:
#         while not shutdown_event.is_set():
#             success, frame = video_capture.read()
#             if not success:
#                 print("Error: Could not read frame.")
#                 time.sleep(0.1)  # Small delay before retry
#                 continue
                
#             # If queue is full, remove oldest item
#             if frame_queue.full():
#                 try:
#                     frame_queue.get_nowait()
#                 except queue.Empty:
#                     pass
                    
#             frame_queue.put(frame)
#             time.sleep(0.01)  # Slight delay to prevent CPU overuse
#     finally:
#         video_capture.release()
#         print("Camera released")

# def generate_frames():
#     """Process frames and generate output stream."""
#     global last_alert_time, previous_drowsy_state
    
#     while not shutdown_event.is_set():
#         try:
#             # Get frame with timeout to allow thread to exit when shutdown
#             frame = frame_queue.get(timeout=1.0)
#             current_time = time.time()
            
#             # Select model and detect drowsiness
#             with drowsy_state_lock:
#                 selected_model = drowsy_state["selected_model"]
            
#             # Detect drowsiness based on selected model
#             try:
#                 if selected_model == "cnn":
#                     is_drowsy, processed_frame = cnn_detector.detect_drowsiness(frame.copy())
#                     with drowsy_state_lock:
#                         drowsy_state["blink_count"] = cnn_detector.blink_count
#                         drowsy_state["yawn_count"] = cnn_detector.yawn_count
#                 else:
#                     is_drowsy, processed_frame = lstm_detector.detect_drowsiness(frame.copy())
#                     with drowsy_state_lock:
#                         drowsy_state["blink_count"] = lstm_detector.blink_count
#                         drowsy_state["yawn_count"] = lstm_detector.yawn_count
#             except Exception as e:
#                 print(f"Error in drowsiness detection: {e}")
#                 # Use original frame if detection fails
#                 processed_frame = frame.copy()
#                 is_drowsy = False
#                 continue
                
#             # Update drowsy state with lock
#             with drowsy_state_lock:
#                 drowsy_state["drowsy"] = is_drowsy
#                 local_prev_drowsy = previous_drowsy_state
#                 previous_drowsy_state = is_drowsy
            
#             # Generate alert if needed
#             state_changed = is_drowsy and not local_prev_drowsy
#             time_elapsed = current_time - last_alert_time >= alert_interval
            
#             if is_drowsy and (state_changed or time_elapsed):
#                 print(f"Triggering alert: state_changed={state_changed}, time_elapsed={time_elapsed}")
#                 # Update last_alert_time before speaking to prevent rapid alerts if speech takes time
#                 last_alert_time = current_time
#                 voice.speak("Warning: You appear to be drowsy. Please stay alert!")
                
#             # Add status text on frame
#             status_text = f"Status: {'DROWSY' if is_drowsy else 'ALERT'}"
#             cv2.putText(processed_frame, status_text, (10, 30), 
#                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if is_drowsy else (0, 255, 0), 2)
                
#             # Encode frame
#             ret, buffer = cv2.imencode('.jpg', processed_frame)
#             if not ret:
#                 continue
                
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
#         except queue.Empty:
#             # Just continue if no frame is available
#             continue
#         except Exception as e:
#             print(f"Error processing frame: {e}")
#             time.sleep(0.1)  # Add delay to prevent rapid error looping

# @app.route('/video')
# def video_feed():
#     """Stream the processed video feed."""
#     return Response(generate_frames(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame', 
#                     headers={'Cache-Control': 'no-cache, no-store, must-revalidate'})

# @app.route('/status')
# def get_status():
#     """Return drowsiness status."""
#     with drowsy_state_lock:
#         current_state = drowsy_state.copy()
#     return jsonify(current_state)

# @app.route('/select_model', methods=['POST'])
# def select_model():
#     """Handle model selection."""
#     model = request.json.get('model')
#     if model in ['cnn', 'lstm']:
#         with drowsy_state_lock:
#             drowsy_state["selected_model"] = model
#         # Reset detectors
#         cnn_detector.reset()
#         lstm_detector.reset()
#         return jsonify({"status": "success", "model": model})
#     return jsonify({"status": "error", "message": "Invalid model"}), 400

# def cleanup():
#     """Release resources properly."""
#     print("Starting cleanup...")
#     shutdown_event.set()  # Signal threads to terminate
#     try:
#         voice.stop()
#     except Exception as e:
#         print(f"Error stopping VoiceAssistant: {e}")

# if __name__ == '__main__':
#     # Start frame capture thread
#     capture_thread = threading.Thread(target=capture_frames)
#     capture_thread.daemon = True
#     capture_thread.start()
    
#     try:
#         app.run(host='localhost', port=5000, threaded=True)
#     except KeyboardInterrupt:
#         print("Shutting down Flask server...")
#     finally:
#         cleanup()
#         # Give threads time to clean up
#         time.sleep(1)
import os
from flask import Flask, Response, jsonify, request
import cv2
import time
import threading
import queue

# Import all three detectors
from src.drowsiness_detector import DrowsinessDetector
from src.drowsiness_detector_lstm import DrowsinessDetectorLSTM
from src.drowsiness_detector_ear import DrowsinessDetectorEAR
from src.voice_assistant import VoiceAssistant

app = Flask(__name__)

# Initialize detectors and voice assistant
cnn_detector = DrowsinessDetector()
lstm_detector = DrowsinessDetectorLSTM()

base_dir = os.path.dirname(os.path.abspath(__file__))
# Point predictor_path to wherever your .dat lives
ear_detector = DrowsinessDetectorEAR(
    predictor_path=os.path.join(base_dir,"src" , "models", "shape_predictor_68_face_landmarks.dat"),
    ear_threshold=0.20,
    ear_consec_frames=30,
    mar_threshold=0.35,
    mar_consec_frames=15,
    cooldown_secs=2.0
)
voice = VoiceAssistant()

# Global state with thread safety
drowsy_state_lock = threading.Lock()
drowsy_state = {
    "drowsy": False,
    "blink_count": 0,
    "yawn_count": 0,
    "selected_model": "cnn"
}

# Frame queue & control
frame_queue     = queue.Queue(maxsize=5)
last_alert_time = 0
alert_interval  = 1  # seconds
previous_drowsy_state = False
shutdown_event  = threading.Event()

def capture_frames():
    """Continuously read from webcam into a queue."""
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return

    try:
        while not shutdown_event.is_set():
            ret, frame = video_capture.read()
            if not ret:
                time.sleep(0.1)
                continue

            if frame_queue.full():
                try:
                    frame_queue.get_nowait()
                except queue.Empty:
                    pass

            frame_queue.put(frame)
            time.sleep(0.01)
    finally:
        video_capture.release()

def generate_frames():
    """Consume frames, run the selected detector, stream MJPEG."""
    global last_alert_time

    while not shutdown_event.is_set():
        try:
            frame = frame_queue.get(timeout=1.0)
            t0    = time.time()

            # Pick model
            with drowsy_state_lock:
                model = drowsy_state["selected_model"]

            # Run detection
            try:
                if model == "cnn":
                    is_d, proc = cnn_detector.detect_drowsiness(frame.copy())
                    bc = cnn_detector.blink_count
                    yc = cnn_detector.yawn_count

                elif model == "lstm":
                    is_d, proc = lstm_detector.detect_drowsiness(frame.copy())
                    bc = lstm_detector.blink_count
                    yc = lstm_detector.yawn_count

                else:  # EAR mode
                    is_d, proc = ear_detector.detect(frame.copy())
                    # EAR mode only has a closed‐frame counter
                    bc = ear_detector.eye_closed_cnt

                    yc = ear_detector.yawn_open_cnt
                    

                # Update global counters
                with drowsy_state_lock:
                    drowsy_state["drowsy"]       = is_d
                    drowsy_state["blink_count"]  = bc
                    drowsy_state["yawn_count"]   = yc

            except Exception as e:
                print(f"Error in drowsiness detection: {e}")
                proc = frame.copy()
                is_d = False
                with drowsy_state_lock:
                    drowsy_state["drowsy"]      = False
                    drowsy_state["blink_count"] = 0
                    drowsy_state["yawn_count"]  = 0

            # Voice alert logic (on rising edge or interval)
            # became_drowsy = is_d 
            timed_ok      = (t0 - last_alert_time) >= alert_interval
            if is_d and timed_ok:
                last_alert_time = t0
                voice.speak("Warning: You appear to be drowsy. Please stay alert!")


            # Annotate status
            status_txt = "DROWSY" if is_d else "AWAKE"
            color      = (0,0,255) if is_d else (0,255,0)
            cv2.putText(proc, f"Status: {status_txt}", (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Stream it
            ok, buf = cv2.imencode('.jpg', proc)
            if not ok:
                continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')

        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error processing frame: {e}")
            time.sleep(0.1)

@app.route('/video')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame',
                    headers={'Cache-Control': 'no-cache, no-store'})

@app.route('/status')
def get_status():
    with drowsy_state_lock:
        return jsonify(drowsy_state)

@app.route('/select_model', methods=['POST'])
def select_model():
    m = request.json.get('model')
    if m in ('cnn','lstm','ear'):
        with drowsy_state_lock:
            drowsy_state["selected_model"] = m
        # reset all detectors
        cnn_detector.reset()
        lstm_detector.reset()
        ear_detector.reset()
        return jsonify(status="success", model=m)
    return jsonify(status="error", message="Invalid model"), 400

def cleanup():
    shutdown_event.set()
    try: voice.stop()
    except: pass

if __name__=='__main__':
    # Start the capture thread
    t = threading.Thread(target=capture_frames, daemon=True)
    t.start()

    try:
        app.run(host='localhost', port=5000, threaded=True)
    finally:
        cleanup()
        time.sleep(1)
