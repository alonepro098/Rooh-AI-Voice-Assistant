# 🎙️ ROOH AI - Advanced Voice-Controlled JARVIS Desktop Assistant

**Rooh** is a sleek, intelligent voice-controlled personal desktop assistant with a **sweet Indian female voice** (`hi-IN-SwaraNeural`), **Google Gemini AI Studio API Integration**, and full Windows desktop automation capabilities.

---

## ✨ Features

1. **Voice Activation & Wake Words**:
   - Responds to `"Hello Rooh"`, `"Rooh"`, `"Rooh Udhar"`, or manual clap sound triggers.
   - Continuous background listening with multi-language recognition (`hi-IN` Hindi & `en-IN` English).

2. **Sweet Indian Female Voice (TTS)**:
   - Powered by Microsoft Edge Neural Speech Engine (`hi-IN-SwaraNeural`) delivering a thin, sweet Indian girl's voice tone.
   - Fast, zero-lag native Windows playback via MCI (`winmm.dll`).

3. **Notepad Dictation & Auto-Save**:
   - Command: *"Notepad kholo aur likho [text] aur save karo"*
   - Dynamically opens Notepad, types or saves the dictated content, and saves the `.txt` file automatically on your Desktop!

4. **YouTube Music Auto Search & Play**:
   - Command: *"YouTube par song sunao Tum Hi Ho"* or *"yt par song sunao [song name]"*
   - Searches YouTube and automatically begins video playback!

5. **App Launcher**:
   - Opens apps & websites instantly:
     - **WhatsApp**: *"WhatsApp kholo"*
     - **YouTube**: *"YouTube kholo"*
     - **Notepad**: *"Notepad kholo"*
     - **Chrome**: *"Chrome kholo"*
     - **Calculator**: *"Calculator kholo"*
     - **VS Code**: *"VS Code kholo"*
     - **Paint**, **File Explorer**, **Settings**, **Command Prompt**, etc.

6. **Google AI Studio Integration (Gemini 3.6 Flash)**:
   - Configured with your Gemini API Key (`AQ.Ab8RN6...`).
   - Generates smart, sweet, and context-aware conversational answers to any general knowledge question or conversation prompt.

7. **System Controls & Utilities**:
   - Volume control (*"volume badhao"*, *"volume kam karo"*, *"mute karo"*)
   - Screenshots (*"screenshot lo"*)
   - Date & Time (*"time kya hua hai"*, *"aaj konsi date hai"*)
   - Google Searches (*"google par search karo [query]"*)

8. **Futuristic Glowing JARVIS Dashboard UI**:
   - Animated Glowing Core Arc Reactor & audio equalizer waveform animation.
   - Live Command & Conversation Log.
   - Manual text box & Voice Mic toggle button.

---

## 🚀 How to Run

### Method 1: Double Click Launcher
Double click `launcher.bat` in the project directory.

### Method 2: Command Prompt / Terminal
Run the following command:
```bash
python main.py
```

---

## 📁 File Structure

- `main.py` - Core application entry point & event loop
- `gui_dashboard.py` - Glowing JARVIS Tkinter GUI interface
- `tts_engine.py` - Sweet Indian Female Voice TTS engine
- `stt_engine.py` - Microphone listener & wake word parser
- `ai_brain.py` - Google Gemini AI Studio integration
- `command_handler.py` - App launcher, Notepad dictation, and YouTube music automation
- `config.py` - Assistant configuration, API keys, and app mappings
- `launcher.bat` - One-click launcher script
