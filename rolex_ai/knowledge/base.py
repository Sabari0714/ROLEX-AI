class LocalKnowledge:
    def __init__(self): self.items={}
    def add(self,key,value): self.items[str(key)]=value
    def get(self,key,default=None): return self.items.get(str(key),default)
    def status(self): return {'module':'Local Knowledge','status':'READY','entries':len(self.items)}
