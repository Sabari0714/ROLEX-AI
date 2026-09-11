from .personal_intelligence import PersonalIntelligence
from .multi_agent import MultiAgent
from .autonomous_executor import AutonomousExecutor
class LocalBrain:
    VERSION='1.0-local'
    def __init__(self,db,memory,router,tools,autonomous=None):
        self.db=db; self.memory=memory; self.router=router; self.tools=tools; self.autonomous=autonomous; self.personal=PersonalIntelligence(db,memory); self.multi_agent=MultiAgent(); self.autonomous_executor=AutonomousExecutor()
    def attach_voice(self,x): self.voice=x
    def attach_vision(self,x): self.vision=x
    def attach_web(self,x): self.web=x
    def attach_self_repair(self,x): self.self_repair=x
    def attach_communication(self,x): self.communication=x
    def answer(self,text):
        raw=str(text or '').strip(); low=raw.lower()
        self.db.add_message('user',raw)
        if low.startswith('remember ') or low.startswith('please remember '):
            value=raw.split(' ',1)[1] if ' ' in raw else raw; self.memory.remember(value); out=f'நினைவில் வைத்துக்கொண்டேன்: {value}'
        elif low in {'memory','show memory','what do you remember'}:
            out=str(self.memory.all_memories(limit=20))
        elif hasattr(self.tools,'math') and self.tools.math.can_handle(raw): out=str(self.tools.math.calculate(raw))
        elif low in {'hello','hi','vanakkam','வணக்கம்'}: out='Vanakkam boss. Rolex AI online.'
        elif 'status' in low: out='ROLEX AI | local brain: READY | memory: READY | math: READY'
        else: out=f'ROLEX: Command received — {raw}'
        self.db.add_message('assistant',out); return out
    def status(self): return {'version':self.VERSION,'local_only':True,'personal_intelligence':self.personal.status()}
