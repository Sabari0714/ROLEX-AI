class Scheduler:
    def __init__(self,db): self.db=db; self.jobs={}
    def add(self,name,fn,*args,**kwargs): self.jobs[name]=(fn,args,kwargs)
    def run(self,name):
        item=self.jobs.get(name); return item[0](*item[1],**item[2]) if item else None
    def status(self): return {'status':'READY','jobs':len(self.jobs)}
