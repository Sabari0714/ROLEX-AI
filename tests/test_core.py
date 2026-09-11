import os,tempfile,unittest
from pathlib import Path
from rolex_ai.app import RolexAI
from rolex_ai.storage.db import Database
from rolex_ai.core.memory import MemoryManager
from rolex_ai.tools.math_engine import MathEngine

class TestRolexCore(unittest.TestCase):
    def test_math(self):
        m=MathEngine(); self.assertEqual(m.calculate('12*2'),24); self.assertEqual(m.calculate('(10+5)*2'),30); self.assertEqual(m.calculate('12^2'),144); self.assertEqual(m.calculate('10/2'),5)
    def test_invalid(self): self.assertIsNone(MathEngine().calculate('os.system("x")'))
    def test_memory(self):
        with tempfile.TemporaryDirectory() as d:
            db=Database(Path(d)/'r.db'); mm=MemoryManager(db); mm.remember('Rolex uses local memory'); self.assertEqual(len(mm.recall('local memory')),1)
    def test_app_status(self):
        old=os.environ.get('ROLEX_UI'); os.environ['ROLEX_UI']='0'
        try:
            ai=RolexAI(); self.assertEqual(ai.status()['app'],'ROLEX AI'); self.assertIn('ROLEX AI',ai.ask('status'))
        finally:
            if old is None: os.environ.pop('ROLEX_UI',None)
            else: os.environ['ROLEX_UI']=old

if __name__=='__main__':unittest.main()
