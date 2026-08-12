import time
import speech_recognition as sr
import config

class STTEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 1200
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.is_listening = False

    def listen_command(self, status_callback=None):
        """Listen to microphone input and convert speech to text"""
        with sr.Microphone() as source:
            print("[STT Engine]: Adjusting ambient noise...")
            if status_callback:
                status_callback("Adjusting noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)

            print("[STT Engine]: Listening for voice or clap...")
            if status_callback:
                status_callback("Listening...")

            self.is_listening = True
            try:
                audio = self.recognizer.listen(
                    source, 
                    timeout=config.LISTEN_TIMEOUT, 
                    phrase_time_limit=config.PHRASE_TIME_LIMIT
                )
                if status_callback:
                    status_callback("Processing speech...")

                # Check audio sound energy for clap detection
                raw_data = audio.get_raw_data()
                energy = sum(abs(int.from_bytes(raw_data[i:i+2], byteorder='little', signed=True)) for i in range(0, min(1000, len(raw_data)-1), 2)) / 500
                print(f"[STT Energy Level]: {energy}")

                # Try Hindi / Hinglish recognition first
                try:
                    text = self.recognizer.recognize_google(audio, language="hi-IN")
                    print(f"[STT Recognized (hi-IN)]: {text}")
                    return text.strip()
                except sr.UnknownValueError:
                    try:
                        text = self.recognizer.recognize_google(audio, language="en-IN")
                        print(f"[STT Recognized (en-IN)]: {text}")
                        return text.strip()
                    except sr.UnknownValueError:
                        # If energy spike sound like a clap happened
                        if energy > config.CLAP_THRESHOLD:
                            print("[Clap Sound Energy Detected!]")
                            return "CLAP_TRIGGER"
                        return ""

            except sr.WaitTimeoutError:
                print("[STT Engine]: Listening timeout.")
                return ""
            except sr.RequestError as e:
                print(f"[STT Google API Error]: {e}")
                return ""
            except Exception as e:
                print(f"[STT Error]: {e}")
                return ""
            finally:
                self.is_listening = False
                if status_callback:
                    status_callback("Idle")

    def check_wake_word(self, text):
        """Check if wake word 'Hello Rooh' or 'Rooh' or 'CLAP_TRIGGER' is detected"""
        if not text:
            return False
        if text == "CLAP_TRIGGER":
            return True
        text_lower = text.lower()
        for wake in config.WAKE_WORDS:
            if wake in text_lower:
                return True
        return False

# Global STT Instance
stt = STTEngine()
