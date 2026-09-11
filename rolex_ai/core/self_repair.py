class SelfRepairEngine:
    def __init__(self,root_dir=None,db=None,policy=None): self.root_dir=root_dir; self.db=db; self.policy=policy
    def status(self):return {'status':'READY','sandbox_required':True}
