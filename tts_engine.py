import asyncio
import os
import time
import ctypes
import tempfile
import threading
import requests
import edge_tts
import pyttsx3
import config

class TTSEngine:
    def __init__(self):
        self.voice = config.TTS_VOICE
        self.rate = config.TTS_RATE
        self.pitch = config.TTS_PITCH
        self.is_speaking = False
        self.winmm = ctypes.windll.winmm
        
        # Offline fallback setup
        try:
            self.offline_engine = pyttsx3.init()
            voices = self.offline_engine.getProperty('voices')
            for v in voices:
                if "female" in v.name.lower() or "zira" in v.name.lower() or "heera" in v.name.lower():
                    self.offline_engine.setProperty('voice', v.id)
                    break
        except Exception:
            self.offline_engine = None

    def _play_audio_winmm(self, filepath):
        """Play audio using native Windows winmm.dll MCI interface"""
        try:
            alias = f"rooh_audio_{int(time.time()*1000)}"
            open_cmd = f'open "{filepath}" type mpegvideo alias {alias}'
            self.winmm.mciSendStringW(open_cmd, None, 0, 0)
            
            play_cmd = f'play {alias} wait'
            self.winmm.mciSendStringW(play_cmd, None, 0, 0)
            
            close_cmd = f'close {alias}'
            self.winmm.mciSendStringW(close_cmd, None, 0, 0)
        except Exception as e:
            print(f"[TTS Audio Error]: {e}")

    def _generate_elevenlabs(self, text, temp_path):
        """ElevenLabs Custom Cloned Voice API Generator"""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{config.ELEVENLABS_VOICE_ID}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": config.ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.85
            }
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(temp_path, "wb") as f:
                f.write(response.content)
            return True
        return False

    async def _generate_and_play(self, text, callback_on_start=None, callback_on_end=None):
        """Generate audio (via ElevenLabs or Pitch-tuned Edge TTS) and play"""
        temp_path = os.path.join(tempfile.gettempdir(), f"rooh_speech_{int(time.time()*1000)}.mp3")
        try:
            self.is_speaking = True
            if callback_on_start:
                callback_on_start()

            # Try ElevenLabs Voice Cloning if Key & Voice ID are provided
            audio_ready = False
            if config.TTS_ENGINE_TYPE == "elevenlabs" and config.ELEVENLABS_API_KEY and config.ELEVENLABS_VOICE_ID:
                try:
                    audio_ready = self._generate_elevenlabs(text, temp_path)
                except Exception as e:
                    print(f"[ElevenLabs TTS Error, falling back to Edge TTS]: {e}")

            # Fallback to pitch-tuned Edge TTS (Soft, Melodic, Cute Indian Voice)
            if not audio_ready:
                communicate = edge_tts.Communicate(
                    text=text,
                    voice=self.voice,
                    rate=self.rate,
                    pitch=self.pitch
                )
                await communicate.save(temp_path)

            # Play audio on thread
            play_thread = threading.Thread(target=self._play_audio_winmm, args=(temp_path,), daemon=True)
            play_thread.start()
            play_thread.join()

        except Exception as e:
            print(f"[TTS Error, trying offline fallback]: {e}")
            self._speak_offline(text)
        finally:
            self.is_speaking = False
            if callback_on_end:
                callback_on_end()
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

    def _speak_offline(self, text):
        if self.offline_engine:
            try:
                self.offline_engine.say(text)
                self.offline_engine.runAndWait()
            except Exception as e:
                print(f"[Offline TTS Error]: {e}")

    def speak(self, text, callback_on_start=None, callback_on_end=None, blocking=True):
        if not text or not text.strip():
            return
            
        print(f"[Rooh]: {text}")
        
        def run():
            asyncio.run(self._generate_and_play(text, callback_on_start, callback_on_end))

        if blocking:
            run()
        else:
            t = threading.Thread(target=run, daemon=True)
            t.start()

# Global TTS Instance
tts = TTSEngine()

if __name__ == "__main__":
    tts.speak("Suno... mujhe neend aati nahi hai... main aapke saath hoon master...")
