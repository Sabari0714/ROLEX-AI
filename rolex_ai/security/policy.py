class SecurityPolicy:
    def __init__(self,local_only=True,allow_external_ai=False): self.local_only=bool(local_only); self.allow_external_ai=bool(allow_external_ai) and not self.local_only
    def status(self): return {'local_only':self.local_only,'allow_external_ai':self.allow_external_ai,'status':'READY'}
