import os

# Google AI Studio Gemini API Key
# Put your Gemini API Key here or set GEMINI_API_KEY environment variable
DEFAULT_KEY = "AQ.Ab8RN6" + "KrXjH5JVUGZa9hAb2ZPr-sA3qLadzFbLw2Yc1Jryt54w"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", DEFAULT_KEY)
GEMINI_MODEL = "gemini-3.6-flash"

# TTS Engine Type: "edge_tts" (Free Built-in) or "elevenlabs" (Exact Voice Clone)
TTS_ENGINE_TYPE = "edge_tts"

# Voice Settings - Tuned to match the soft, breathy, melodic YouTube girl voice
TTS_VOICE = "hi-IN-SwaraNeural"
TTS_RATE = "-12%"
TTS_PITCH = "+16Hz"  # +16Hz pitch for cute soft girl vocal tone

# Optional ElevenLabs Voice Cloning Settings
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "")

# Assistant & User Identity
ASSISTANT_NAME = "Rooh"
USER_NAME = "Ayush"
WAKE_WORDS = ["rooh", "hello rooh", "hey rooh", "udhar", "rooh udhar", "rooh suno", "cute rooh"]

# Clap & Audio Detection Thresholds
CLAP_THRESHOLD = 2500
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 8

# App Paths & Shortcuts Mapping
APP_COMMANDS = {
    "whatsapp": {
        "url": "https://web.whatsapp.com",
        "app_cmd": "whatsapp:",
        "aliases": ["whatsapp", "whatsaap", "wa"]
    },
    "youtube": {
        "url": "https://www.youtube.com",
        "aliases": ["youtube", "yt", "yu tub"]
    },
    "notepad": {
        "app_cmd": "notepad.exe",
        "aliases": ["notepad", "note pad", "notes"]
    },
    "chrome": {
        "app_cmd": "chrome.exe",
        "url": "https://www.google.com",
        "aliases": ["chrome", "browser", "google chrome"]
    },
    "calculator": {
        "app_cmd": "calc.exe",
        "aliases": ["calculator", "calc", "hisaab"]
    },
    "vscode": {
        "app_cmd": "code",
        "aliases": ["vscode", "vs code", "code editor"]
    },
    "paint": {
        "app_cmd": "mspaint.exe",
        "aliases": ["paint", "ms paint", "drawing"]
    },
    "settings": {
        "app_cmd": "start ms-settings:",
        "aliases": ["settings", "setting", "system settings"]
    },
    "cmd": {
        "app_cmd": "cmd.exe",
        "aliases": ["cmd", "command prompt", "terminal"]
    },
    "file explorer": {
        "app_cmd": "explorer.exe",
        "aliases": ["file explorer", "my computer", "this pc", "files"]
    }
}
