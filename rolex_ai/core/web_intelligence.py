class WebIntelligence:
    def __init__(self,allow_network=False): self.allow_network=bool(allow_network)
    def status(self):return {'status':'READY','network_enabled':self.allow_network}
