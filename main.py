import sys
import time
import threading
import tkinter as tk

import config
from tts_engine import tts
from stt_engine import stt
from ai_brain import brain
from command_handler import cmd_handler
from gui_dashboard import RoohGUI

class RoohAssistantApp:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = RoohGUI(
            self.root, 
            on_mic_click=self.trigger_voice_interaction,
            on_send_text=self.process_text_input
        )
        self.is_processing = False
        self.continuous_listening = True

        # Welcome message on launch
        self.gui.log_message("sys", "Rooh AI Desktop Assistant is active.")
        self.gui.log_message("rooh", "Umm... hello master... main Rooh hoon... aap bataiye main kya karun? Hehe!")

        # Play greeting voice in background thread on startup
        threading.Thread(target=self._greeting_speech, daemon=True).start()

        # Start continuous background listener thread
        self.bg_thread = threading.Thread(target=self._continuous_listener_loop, daemon=True)
        self.bg_thread.start()

    def _greeting_speech(self):
        self.gui.update_state("SPEAKING", "Greeting...")
        tts.speak(f"Hello {config.USER_NAME}! Kaise ho aap? Main toh bas aapka hi wait kar rahi thi!")
        self.gui.update_state("IDLE", "Listening for Clap or 'Hello Rooh'...")

    def trigger_voice_interaction(self):
        """Triggered when user clicks 'SPEAK / LISTEN NOW' button"""
        if self.is_processing:
            return

        self.is_processing = True
        self.gui.update_state("LISTENING", "Listening for your voice command...")
        
        # Listen via microphone
        query = stt.listen_command(status_callback=lambda msg: self.gui.update_state("LISTENING", msg))
        
        if query:
            self.gui.log_message("user", query)
            self._process_command(query)
        else:
            self.gui.log_message("sys", "Koi aawaz nahi sunai di. Please dubara boliye.")
            self.gui.update_state("IDLE", "Idle (Ready)")
            
        self.is_processing = False

    def process_text_input(self, text):
        """Triggered when user types text in GUI text input"""
        if self.is_processing or not text:
            return

        self.is_processing = True
        self.gui.log_message("user", text)
        self._process_command(text)
        self.is_processing = False

    def _process_command(self, query):
        """Process user command via Command Router or Gemini AI"""
        self.gui.update_state("THINKING", "Processing command...")

        # Step 1: Try Local Command Execution (App launcher, Notepad dictation, YouTube music, system controls)
        executed, action_res = cmd_handler.parse_and_execute(query)

        if executed:
            self.gui.log_message("sys", f"Action Executed: {action_res}")
            self.gui.update_state("IDLE", "Command executed successfully.")
            return

        # Step 2: Pass to Gemini AI Studio Brain
        self.gui.update_state("THINKING", "Thinking with Gemini AI...")
        ai_reply = brain.ask(query)

        self.gui.log_message("rooh", ai_reply)
        self.gui.update_state("SPEAKING", "Speaking response...")

        # Speak AI response with sweet Indian female voice
        tts.speak(ai_reply)

        self.gui.update_state("IDLE", "Idle (Ready)")

    def _continuous_listener_loop(self):
        """Continuous background thread listening for clap or 'Hello Rooh'"""
        while self.continuous_listening:
            try:
                if not self.is_processing and not tts.is_speaking:
                    text = stt.listen_command()
                    if text and stt.check_wake_word(text):
                        print(f"[Wake / Clap Triggered]: Spoken text/sound -> '{text}'")
                        self.gui.log_message("sys", f"Wake/Clap detected: '{text}'")
                        
                        # Exact requested response: "Hello Ayush, kaise ho?"
                        reply = f"Hello {config.USER_NAME}, kaise ho aap? Main toh bas aapka hi wait kar rahi thi!"
                        self.gui.log_message("rooh", reply)
                        self.gui.update_state("SPEAKING", "Greeting Ayush...")
                        tts.speak(reply)
                        
                        # Process rest of command if spoken together, or listen for follow up
                        clean_cmd = text
                        if text != "CLAP_TRIGGER":
                            for wake in config.WAKE_WORDS:
                                clean_cmd = clean_cmd.lower().replace(wake, "").strip()
                        
                        if clean_cmd and len(clean_cmd) > 2 and text != "CLAP_TRIGGER":
                            self.gui.log_message("user", clean_cmd)
                            self._process_command(clean_cmd)
                        else:
                            self.trigger_voice_interaction()
            except Exception as e:
                print(f"[Background Listener Loop Exception]: {e}")
            time.sleep(1)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RoohAssistantApp()
    app.run()
