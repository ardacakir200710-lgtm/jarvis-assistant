import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import keyboard
import time

class JarvisEar:
    def __init__(self):
        print("[System] Loading Whisper AI for voice recognition...")
        self.model = WhisperModel("base.en", device="cpu", compute_type="int8")
        self.fs = 16000

    def listen_ptt(self, hotkey='space'):
        print(f"\n[System] Hold '{hotkey.upper()}' key to speak...")
        
        # Tuşa basılana kadar bekle
        keyboard.wait(hotkey)
        print("[Jarvis is listening...]")

        recorded_frames = []
        
        # Ses verisi geldikçe listeye ekleyen asenkron callback fonksiyonu
        def callback(indata, frames, time, status):
            recorded_frames.append(indata.copy())

        # Tuşa basılı tutulduğu sürece kaydet
        stream = sd.InputStream(samplerate=self.fs, channels=1, dtype='float32', callback=callback)
        with stream:
            while keyboard.is_pressed(hotkey):
                time.sleep(0.05)
        
        print("[System] Key released. Transcribing...")
        
        if not recorded_frames:
            return ""

        # Kaydedilen tüm ses parçalarını birleştirip Whisper'a ver
        audio_array = np.concatenate(recorded_frames, axis=0)
        audio_array = np.squeeze(audio_array)

        segments, info = self.model.transcribe(audio_array, beam_size=5)
        user_text = "".join([segment.text for segment in segments])
        
        return user_text.strip()