import pyttsx3


class VoiceAssistant:

    def speak(self, text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        print("Speech completed successfully")