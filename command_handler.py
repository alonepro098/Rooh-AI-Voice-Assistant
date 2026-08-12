import os
import re
import sys
import time
import subprocess
import webbrowser
import pyautogui
import pywhatkit
import config
from tts_engine import tts

class CommandHandler:
    def __init__(self):
        pass

    def parse_and_execute(self, query):
        """Parse user query and trigger corresponding action"""
        if not query or not query.strip():
            return False, ""

        q = query.lower().strip()
        print(f"[Command Router]: Processing query -> '{q}'")

        # 1. NOTEPAD DICTATION & SAVE
        if "notepad" in q and ("likho" in q or "write" in q or "type" in q or "note" in q):
            return self._handle_notepad_dictation(q)

        # 2. YOUTUBE SONG SEARCH & PLAY
        if ("yt" in q or "youtube" in q or "song" in q or "gana" in q) and ("sunao" in q or "play" in q or "chalao" in q or "bajao" in q):
            return self._handle_youtube_song(q)

        # 3. APP LAUNCHER
        if "kholo" in q or "open" in q or "start" in q or "launch" in q:
            return self._handle_app_launcher(q)

        # 4. SYSTEM CONTROL & UTILITIES
        if "volume" in q:
            return self._handle_volume(q)
        if "screenshot" in q:
            return self._handle_screenshot()
        if "time" in q or "samay" in q or "wakt" in q:
            return self._handle_time()
        if "date" in q or "tareekh" in q:
            return self._handle_date()
        if "google" in q and "search" in q:
            return self._handle_google_search(q)
        if "shutdown" in q or "band karo PC" in q:
            return self._handle_shutdown()

        # Not a direct system command -> Pass to Gemini AI
        return False, ""

    def _handle_app_launcher(self, q):
        """Open desktop apps or web apps with cute response"""
        for app_key, app_info in config.APP_COMMANDS.items():
            for alias in app_info["aliases"]:
                if alias in q:
                    tts.speak(f"Umm... ji master! Main {app_key.title()} khol rahi hoon... hehe.")
                    if "url" in app_info:
                        webbrowser.open(app_info["url"])
                    elif "app_cmd" in app_info:
                        try:
                            if app_info["app_cmd"].startswith("start "):
                                os.system(app_info["app_cmd"])
                            else:
                                subprocess.Popen(app_info["app_cmd"], shell=True)
                        except Exception as e:
                            print(f"[App Launch Error]: {e}")
                    return True, f"Opened {app_key}"
        
        # Generic app opening attempt
        words = q.replace("kholo", "").replace("open", "").replace("start", "").replace("launch", "").strip()
        if words:
            tts.speak(f"Umm... main {words} search karke open kar rahi hoon...")
            webbrowser.open(f"https://www.google.com/search?q={words}")
            return True, f"Opened web query: {words}"
        return False, ""

    def _handle_notepad_dictation(self, q):
        """Notepad kholo, likho, aur save karo with cute responses"""
        tts.speak("Umm... ji master! Main Notepad khol kar aapka message pyare se likh rahi hoon...")
        
        # Extract text to write
        text_to_write = ""
        match = re.search(r'(?:likho|write|type)\s+(.*?)(?:\s+aur\s+save|\s+save|$)', q)
        if match:
            text_to_write = match.group(1).strip()
        else:
            text_to_write = q.replace("notepad kholo", "").replace("aur likho", "").replace("likho", "").replace("save karo", "").strip()

        if not text_to_write:
            text_to_write = "Rooh AI Voice Assistant - Special Cute Dictation Note."

        # Desktop folder path
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_name = f"Rooh_Note_{int(time.time())}.txt"
        file_path = os.path.join(desktop_path, file_name)

        # Write text directly to file and launch Notepad
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"--- Note Dictated to Rooh (Cute Assistant) ---\n\n{text_to_write}\n\nDate: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Open the saved file in Notepad
            subprocess.Popen(["notepad.exe", file_path])
            
            tts.speak(f"Umm... likh diya hai master! Desktop par '{file_name}' naam se save bhi kar diya hai!")
            return True, f"Dictated & Saved to Notepad: {file_path}"
        except Exception as e:
            print(f"[Notepad Error]: {e}")
            subprocess.Popen("notepad.exe")
            time.sleep(1)
            pyautogui.typewrite(text_to_write, interval=0.05)
            if "save" in q:
                pyautogui.hotkey('ctrl', 's')
            tts.speak("Likh diya hai master!")
            return True, "Dictated into Notepad"

    def _handle_youtube_song(self, q):
        """YouTube search and auto song playback"""
        clean_q = q.replace("yt", "").replace("youtube", "").replace("par", "").replace("per", "")
        clean_q = clean_q.replace("song", "").replace("gaana", "").replace("gana", "")
        clean_q = clean_q.replace("sunao", "").replace("play", "").replace("chalao", "").replace("bajao", "").strip()

        if not clean_q:
            clean_q = "Tum Hi Ho"

        tts.speak(f"Umm... ji master! YouTube par aapka pyara song '{clean_q}' play kar rahi hoon...")
        try:
            pywhatkit.playonyt(clean_q)
        except Exception as e:
            print(f"[YouTube Error]: {e}")
            search_url = f"https://www.youtube.com/results?search_query={clean_q.replace(' ', '+')}"
            webbrowser.open(search_url)
        return True, f"Playing YouTube song: {clean_q}"

    def _handle_volume(self, q):
        """Volume control"""
        if "up" in q or "badhao" in q or "increase" in q or "zyada" in q:
            for _ in range(5):
                pyautogui.press("volumeup")
            tts.speak("Umm... volume badha diya hai master.")
            return True, "Volume Up"
        elif "down" in q or "kam" in q or "decrease" in q or "ghatao" in q:
            for _ in range(5):
                pyautogui.press("volumedown")
            tts.speak("Umm... volume kam kar diya hai master.")
            return True, "Volume Down"
        elif "mute" in q or "chup" in q:
            pyautogui.press("volumemute")
            tts.speak("Audio mute kar diya hai.")
            return True, "Volume Mute"
        return False, ""

    def _handle_screenshot(self):
        """Take screenshot and save to Pictures folder"""
        pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        filename = os.path.join(pictures_dir, f"Screenshot_Rooh_{int(time.time())}.png")
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            tts.speak("Screenshot le kar Pictures folder mein save kar diya hai master!")
            return True, f"Screenshot saved: {filename}"
        except Exception as e:
            tts.speak("Screenshot lene mein error aaya.")
            return True, f"Screenshot error: {e}"

    def _handle_time(self):
        current_time = time.strftime("%I:%M %p")
        tts.speak(f"Umm... abhi time hua hai {current_time}.")
        return True, f"Time: {current_time}"

    def _handle_date(self):
        current_date = time.strftime("%A, %d %B %Y")
        tts.speak(f"Umm... aaj date hai {current_date}.")
        return True, f"Date: {current_date}"

    def _handle_google_search(self, q):
        query_text = q.replace("google", "").replace("search", "").replace("karo", "").replace("par", "").strip()
        tts.speak(f"Google par '{query_text}' search kar rahi hoon master...")
        webbrowser.open(f"https://www.google.com/search?q={query_text}")
        return True, f"Google searched: {query_text}"

    def _handle_shutdown(self):
        tts.speak("Umm... system 30 seconds mein shutdown ho jayega master...")
        os.system("shutdown /s /t 30")
        return True, "Shutdown scheduled"

# Global Command Handler instance
cmd_handler = CommandHandler()
