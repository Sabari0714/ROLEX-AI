class CommunicationGateway:
    def __init__(self,android=None): self.android=android
    def status(self):return {'status':'READY','android_adapter':bool(self.android)}
