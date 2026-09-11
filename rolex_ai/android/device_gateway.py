class AndroidDeviceGateway:
    def __init__(self,root_dir=None): self.root_dir=root_dir
    def status(self):return {'status':'READY','available':False}
