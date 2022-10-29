import os
import wave
import time
import threading
import tkinter as tk
import pyaudio


class VoiceRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.button = tk.Button(text="🎤", font=(
            "Arial", 120, "bold"), command=self.click_handler)
        self.button.pack()
        self.label = tk.Label(text="Press the button to start recording")
        self.label.pack()
        self.recording = False

        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            # pulsating button

            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1,
                            rate=44100, input=True, frames_per_buffer=1024)
        frames = []
        start = time.time()

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time() - start
            secs = int(passed % 60)
            mins = int(passed // 60)
            hours = int(mins // 60)
            self.label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        self.label.config(text="Saving...")
        exists = True
        i = 1
        while exists:
            if os.path.exists(f"recording{i}.wav"):
                i += 1
            else:
                exists = False

        wave_file = wave.open(f"recording{i}.wav", "wb")
        wave_file.setnchannels(1)
        wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(44100)
        wave_file.writeframes(b"".join(frames))
        wave_file.close()

        self.label.config(text="Press the button to start recording")


VoiceRecorder()
