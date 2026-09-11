class BiometricGateway:
    def authenticate(self,reason='Rolex authentication required'): return {'ok':False,'reason':'unavailable'}
    def status(self): return {'status':'READY','available':False}
