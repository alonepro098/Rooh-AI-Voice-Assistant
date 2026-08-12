import os
import math
import time
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class RoohGUI:
    def __init__(self, root, on_mic_click=None, on_send_text=None):
        self.root = root
        self.on_mic_click = on_mic_click
        self.on_send_text = on_send_text
        
        self.root.title("ROOH AI - Voice Assistant JARVIS Core")
        self.root.geometry("900x680")
        self.root.configure(bg="#0a0b10")
        self.root.resizable(True, True)

        # State Variables
        self.current_state = "IDLE"  # IDLE, LISTENING, THINKING, SPEAKING
        self.anim_angle = 0
        self.is_animating = True

        self._setup_styles()
        self._build_header()
        self._build_center_reactor()
        self._build_status_bar()
        self._build_control_panel()

        # Start animation timer loop
        self._animate_reactor()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('default')

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg="#0d0f18", height=60, bd=0)
        header_frame.pack(fill="x", side="top")

        title_label = tk.Label(
            header_frame, 
            text="ROOH AI  |  INTELLIGENT VOICE ASSISTANT", 
            font=("Segoe UI", 16, "bold"), 
            fg="#00f2fe", 
            bg="#0d0f18", 
            padx=20, 
            pady=12
        )
        title_label.pack(side="left")

        # Status badge
        self.badge_label = tk.Label(
            header_frame,
            text="● SYSTEM READY",
            font=("Segoe UI", 10, "bold"),
            fg="#00ff87",
            bg="#0d0f18",
            padx=20
        )
        self.badge_label.pack(side="right")

    def _build_center_reactor(self):
        main_center = tk.Frame(self.root, bg="#0a0b10")
        main_center.pack(fill="both", expand=True, padx=20, pady=10)

        # Left Canvas for Arc Reactor & Waveform Animation
        left_frame = tk.Frame(main_center, bg="#0f111a", bd=1, relief="solid")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.canvas = tk.Canvas(left_frame, bg="#0f111a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Right Panel for Conversation Log
        right_frame = tk.Frame(main_center, bg="#0f111a", width=400, bd=1, relief="solid")
        right_frame.pack(side="right", fill="both", expand=True)

        chat_title = tk.Label(
            right_frame, 
            text="COMMAND & CONVERSATION LOG", 
            font=("Segoe UI", 11, "bold"), 
            fg="#4facfe", 
            bg="#0f111a", 
            pady=8
        )
        chat_title.pack(fill="x")

        # Scrollable Chat Log Text Area
        self.chat_area = tk.Text(
            right_frame, 
            bg="#08090e", 
            fg="#e0e6ed", 
            font=("Consolas", 10), 
            bd=0, 
            padx=12, 
            pady=12,
            wrap="word"
        )
        self.chat_area.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.chat_area.config(state="disabled")

        # Configure log color tags
        self.chat_area.tag_config("user", foreground="#00f2fe", font=("Consolas", 10, "bold"))
        self.chat_area.tag_config("rooh", foreground="#ff0844", font=("Consolas", 10, "bold"))
        self.chat_area.tag_config("sys", foreground="#00ff87")
        self.chat_area.tag_config("time", foreground="#6c757d")

    def _build_status_bar(self):
        self.status_label = tk.Label(
            self.root, 
            text="Mode: Active Listening | Wake phrase: 'Hello Rooh' | Sweet Indian Voice", 
            font=("Segoe UI", 10), 
            fg="#a0aec0", 
            bg="#0a0b10", 
            pady=6
        )
        self.status_label.pack(fill="x")

    def _build_control_panel(self):
        ctrl_frame = tk.Frame(self.root, bg="#0d0f18", height=80, padx=20, pady=10)
        ctrl_frame.pack(fill="x", side="bottom")

        # Text input field for manual command typing option
        self.text_input = tk.Entry(
            ctrl_frame, 
            bg="#171923", 
            fg="#ffffff", 
            font=("Segoe UI", 11), 
            insertbackground="#00f2fe",
            bd=1,
            relief="flat"
        )
        self.text_input.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=6)
        self.text_input.bind("<Return>", self._on_submit_text)

        # Send Button
        send_btn = tk.Button(
            ctrl_frame, 
            text="SEND", 
            font=("Segoe UI", 10, "bold"), 
            fg="#ffffff", 
            bg="#2b6cb0", 
            activebackground="#3182ce", 
            activeforeground="#ffffff",
            bd=0, 
            padx=15, 
            pady=6,
            cursor="hand2",
            command=self._on_submit_text
        )
        send_btn.pack(side="left", padx=(0, 10))

        # Big Voice Mic Toggle Button
        self.mic_btn = tk.Button(
            ctrl_frame, 
            text="SPEAK / LISTEN NOW", 
            font=("Segoe UI", 11, "bold"), 
            fg="#000000", 
            bg="#00f2fe", 
            activebackground="#4facfe", 
            activeforeground="#000000",
            bd=0, 
            padx=20, 
            pady=6,
            cursor="hand2",
            command=self._on_mic_press
        )
        self.mic_btn.pack(side="right")

    def _on_mic_press(self):
        if self.on_mic_click:
            threading.Thread(target=self.on_mic_click, daemon=True).start()

    def _on_submit_text(self, event=None):
        text = self.text_input.get().strip()
        if text:
            self.text_input.delete(0, tk.END)
            if self.on_send_text:
                threading.Thread(target=self.on_send_text, args=(text,), daemon=True).start()

    def log_message(self, sender, text):
        """Append formatted log message to GUI log"""
        self.chat_area.config(state="normal")
        timestamp = time.strftime("[%H:%M:%S] ")
        self.chat_area.insert(tk.END, timestamp, "time")

        if sender.lower() == "user":
            self.chat_area.insert(tk.END, "YOU: ", "user")
            self.chat_area.insert(tk.END, f"{text}\n")
        elif sender.lower() == "rooh":
            self.chat_area.insert(tk.END, "ROOH: ", "rooh")
            self.chat_area.insert(tk.END, f"{text}\n")
        else:
            self.chat_area.insert(tk.END, f"SYSTEM: {text}\n", "sys")

        self.chat_area.see(tk.END)
        self.chat_area.config(state="disabled")

    def update_state(self, state, status_msg=None):
        """Update JARVIS status and color scheme"""
        self.current_state = state
        if status_msg:
            self.status_label.config(text=f"Status: {status_msg}")

        if state == "LISTENING":
            self.badge_label.config(text="● LISTENING...", fg="#00f2fe")
            self.mic_btn.config(bg="#00f2fe", text="LISTENING...")
        elif state == "THINKING":
            self.badge_label.config(text="● THINKING...", fg="#ff0844")
            self.mic_btn.config(bg="#ff0844", text="THINKING...")
        elif state == "SPEAKING":
            self.badge_label.config(text="● SPEAKING...", fg="#ffb199")
            self.mic_btn.config(bg="#ffb199", text="SPEAKING...")
        else:
            self.badge_label.config(text="● IDLE (READY)", fg="#00ff87")
            self.mic_btn.config(bg="#00f2fe", text="SPEAK / LISTEN NOW")

    def _animate_reactor(self):
        """Draw dynamic glowing arc reactor animation and audio wave visualizer"""
        if not self.canvas.winfo_exists():
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w > 10 and h > 10:
            cx, cy = w / 2, h / 2 - 20
            self.canvas.delete("all")

            # Pulse size depending on state
            pulse = math.sin(self.anim_angle) * 8
            base_radius = 80 + pulse

            # State Colors
            color_primary = "#00f2fe"
            color_secondary = "#4facfe"

            if self.current_state == "LISTENING":
                color_primary = "#00f2fe"
                color_secondary = "#00ff87"
                base_radius += math.sin(self.anim_angle * 3) * 15
            elif self.current_state == "THINKING":
                color_primary = "#ff0844"
                color_secondary = "#ffb199"
                base_radius += math.cos(self.anim_angle * 4) * 12
            elif self.current_state == "SPEAKING":
                color_primary = "#ffb199"
                color_secondary = "#f6d365"
                base_radius += math.sin(self.anim_angle * 5) * 18

            # Outer glowing rings
            for r, alpha_color in [(base_radius + 40, "#1a365d"), (base_radius + 25, "#2b6cb0"), (base_radius + 10, color_secondary)]:
                self.canvas.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    outline=alpha_color, width=2
                )

            # Rotating Arc Segments
            num_arcs = 8
            for i in range(num_arcs):
                start_angle = (i * 45 + self.anim_angle * 50) % 360
                extent = 25
                self.canvas.create_arc(
                    cx - base_radius, cy - base_radius, cx + base_radius, cy + base_radius,
                    start=start_angle, extent=extent,
                    outline=color_primary, width=4, style="arc"
                )

            # Inner Core Circle
            core_r = 35 + math.sin(self.anim_angle * 2) * 5
            self.canvas.create_oval(
                cx - core_r, cy - core_r, cx + core_r, cy + core_r,
                fill=color_primary, outline="#ffffff", width=2
            )

            # Text inside Core
            self.canvas.create_text(
                cx, cy, 
                text="ROOH", 
                font=("Segoe UI", 12, "bold"), 
                fill="#000000"
            )

            # Audio Equalizer Waveforms at the bottom of canvas
            wave_y = h - 40
            bars = 30
            bar_width = (w - 60) / bars

            for b in range(bars):
                bx = 30 + b * bar_width
                if self.current_state != "IDLE":
                    bar_h = abs(math.sin(self.anim_angle * 3 + b * 0.5)) * 40 + 5
                else:
                    bar_h = abs(math.sin(self.anim_angle + b * 0.2)) * 10 + 3

                self.canvas.create_line(
                    bx, wave_y, bx, wave_y - bar_h,
                    fill=color_primary if b % 2 == 0 else color_secondary,
                    width=3
                )

            self.anim_angle += 0.08

        self.root.after(30, self._animate_reactor)

if __name__ == "__main__":
    root = tk.Tk()
    app = RoohGUI(root)
    app.log_message("system", "Rooh JARVIS UI Loaded Successfully!")
    app.log_message("user", "Hello Rooh, WhatsApp kholo")
    app.log_message("rooh", "Ji! Main WhatsApp open kar rahi hoon.")
    root.mainloop()
