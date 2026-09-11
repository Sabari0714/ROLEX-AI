def android_available():
    try: import jnius; return True
    except Exception:return False
class AndroidSTT:
    def listen(self): raise RuntimeError('Android speech recognizer adapter requires Android runtime')
class AndroidTTS:
    def speak(self,text): return False
