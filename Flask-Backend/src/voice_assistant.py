import pyttsx3
import threading

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate  # Adjust speech speed)', 150)  # Adjust speech rate
        self.engine.setProperty('volume', 0.9)   # Adjust volume
        self.lock = threading.Lock()           # Create a lock for thread safety

    def speak(self, text):
        def speak_thread():
            with self.lock:
                self.engine.say(text)
                self.engine.runAndWait()
        threading.Thread(target=speak_thread).start()