import pyttsx3
import keyboard
import multiprocessing
import time

def _speak_worker(text):
    """Bu fonksiyon ana programdan tamamen bağımsız, yalıtılmış bir arka plan işleminde çalışır."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

class JarvisVoice:
    def __init__(self):
        self.process = None

    def speak(self, text):
        # Eğer sistem halihazırda konuşuyorsa önce onu zorla sustur
        self.stop()
        
        # Sesi ana programı kilitlemeden bağımsız bir Process (İşlem) olarak başlat
        self.process = multiprocessing.Process(target=_speak_worker, args=(text,))
        self.process.start()
        
        # Konuşma kendiliğinden bitene VEYA kullanıcı ESC'ye basana kadar sistemi beklemede tut
        while self.process.is_alive():
            if keyboard.is_pressed('esc'):
                print("\n[System] Voice interrupted by user.")
                self.stop()  # İşlemi öldür
                break
            time.sleep(0.05) # İşlemciyi (CPU) yormamak için mikro bekleme

    def stop(self):
        # Arka plandaki konuşma işlemini anında ve kalıcı olarak sonlandır
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process.join()