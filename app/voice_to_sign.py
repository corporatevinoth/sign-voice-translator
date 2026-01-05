import json
import os
import queue
import sounddevice as sd
import vosk
import sys
import threading
from app.utils.tts_engine import speak

class VoiceTranslator:
    def __init__(self):
        self.model_path = "models/vosk-model"
        self.q = queue.Queue()
        self.running = False
        self.thread = None
        
        # Load gloss map
        self.gloss_map_path = os.path.join("data", "gloss_map.json")
        try:
            with open(self.gloss_map_path, "r") as f:
                self.gloss_map = json.load(f)
        except Exception:
            self.gloss_map = {}
            
        # Initial check for model
        if not os.path.exists(self.model_path):
            print(f"Warning: Vosk model not found at {self.model_path}")
            self.model = None
        else:
            try:
                self.model = vosk.Model(self.model_path)
            except Exception as e:
                print(f"Failed to load Vosk model: {e}")
                self.model = None

    def _callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def _listen_loop(self):
        if not self.model:
            return

        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self._callback):
            rec = vosk.KaldiRecognizer(self.model, 16000)
            while self.running:
                try:
                    data = self.q.get(timeout=1) # Non-blocking with timeout to allow checking self.running
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get('text', '')
                        if text:
                            yield text
                except queue.Empty:
                    pass

    # Note: Integrating helper generator into a method we can poll or use a separate queue for results
    def start_listening(self, result_queue):
        if not self.model:
            return
        
        self.running = True
        
        def run():
            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                   channels=1, callback=self._callback):
                rec = vosk.KaldiRecognizer(self.model, 16000)
                while self.running:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get('text', '')
                        if text:
                            result_queue.put(text)
                            self.process_text(text)

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()

    def process_text(self, text):
        words = text.lower().split()
        for word in words:
            if word in self.gloss_map:
                # Logic to trigger animation in UI (handled by checking result_queue in UI)
                pass

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
