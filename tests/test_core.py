import unittest
from main import RolexAI, MathEngine

class TestRolexCore(unittest.TestCase):
    def test_math(self):
        self.assertEqual(MathEngine().calculate('12*2'),24)
        self.assertEqual(MathEngine().calculate('(10+5)*2'),30)
        self.assertEqual(MathEngine().calculate('12^2'),144)
        self.assertEqual(MathEngine().calculate('10/2'),5)
    def test_invalid(self):
        self.assertIsNone(MathEngine().calculate('os.system("x")'))
    def test_brain(self):
        ai=RolexAI(); self.assertIn('ROLEX AI',ai.ask('status'))
    def test_memory(self):
        ai=RolexAI(); ai.remember_test='ok'
        self.assertIsInstance(ai.memory.recent(),list)

if __name__=='__main__': unittest.main()
