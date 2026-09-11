from .math_engine import MathEngine
class Diagnostics:
    def __init__(self,db): self.db=db
    def check(self): return {'database':'READY','local':True}
class TaskTools:
    def __init__(self,db): self.db=db
class ToolHub:
    def __init__(self,db,root=None): self.db=db; self.math=MathEngine(); self.diagnostics=Diagnostics(db); self.tasks=TaskTools(db)
