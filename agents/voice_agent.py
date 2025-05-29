import speech_recognition as sr
import pyttsx3
import logging

logger = logging.getLogger("voice_agent")

class VoiceAgent:
    """
    Handles voice input and output for the finance assistant.
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty("rate", 150)  # Speech rate

    def listen(self, timeout: int = 5) -> str:
        """
        Listen to microphone and return recognized text.
        """
        with sr.Microphone() as source:
            logger.info("Listening for voice input...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized speech: {text}")
                return text
            except sr.WaitTimeoutError:
                logger.warning("Listening timed out while waiting for phrase to start")
                return ""
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return ""
            except sr.RequestError as e:
                logger.error(f"Speech recognition request failed: {e}")
                return ""

    def speak(self, text: str):
        """
        Convert text to speech.
        """
        logger.info(f"Speaking: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
