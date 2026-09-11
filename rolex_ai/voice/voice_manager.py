class VoiceManager:
    def __init__(self): self.listener=None; self.speaker=None; self.enabled=False
    def configure(self,listener=None,speaker=None,enabled=None):
        if listener is not None:self.listener=listener
        if speaker is not None:self.speaker=speaker
        if enabled is not None:self.enabled=bool(enabled)
        return self.status()
    def run_once(self,brain):
        if not self.listener:return 'Voice input unavailable.'
        text=self.listener.listen(); return brain.answer(text) if text else 'No speech detected.'
    def status(self):return {'status':'READY','enabled':self.enabled,'listener':bool(self.listener),'speaker':bool(self.speaker)}
