from pathlib import Path
import hashlib,mimetypes
class VisionManager:
    VERSION='8.0'
    def __init__(self,root_dir=None,**kwargs): self.root_dir=Path(root_dir).resolve() if root_dir else None; self.last_result=None
    def status(self):return {'version':self.VERSION,'status':'READY','local_only':True}
    def analyze(self,image_path):
        p=Path(image_path).expanduser().resolve()
        if self.root_dir:
            try:p.relative_to(self.root_dir)
            except ValueError:raise ValueError('image path outside allowed vision root')
        if not p.is_file():raise FileNotFoundError(p)
        r={'ok':True,'image':str(p),'size_bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mime':mimetypes.guess_type(p.name)[0]}; self.last_result=r; return r
