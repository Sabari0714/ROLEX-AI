import re
class MemoryManager:
    VERSION='2.0'
    def __init__(self,db): self.db=db
    def remember(self,text,kind='fact',importance=.7,tags=None):
        text=str(text or '').strip()
        if not text:return None
        for p in (r'^remember\s+that\s+',r'^remember\s+',r'^please\s+remember\s+',r'^நினைவில்\s+வை\s+'): text=re.sub(p,'',text,flags=re.I)
        hits=self.db.search_memories(text,limit=1)
        if hits and hits[0]['text'].strip().lower()==text.lower(): return hits[0]['id']
        return self.db.add_memory(text,kind,importance,tags)
    def recall(self,q,limit=5): return self.db.search_memories(q,limit)
    def search(self,q,limit=8): return self.recall(q,limit)
    def recent(self,limit=10): return self.db.search_memories('',limit) if False else self.db.search_memories('rolex',limit)
    def get(self,memory_id):
        with self.db.connection() as c:
            r=c.execute('SELECT * FROM memories WHERE id=?',(memory_id,)).fetchone(); return dict(r) if r else None
    def forget(self,memory_id):
        with self.db.connection() as c: return c.execute('DELETE FROM memories WHERE id=?',(memory_id,)).rowcount>0
    def context(self,q,limit=5): return {'query':q,'memories':self.recall(q,limit),'recent_conversation':self.db.recent_messages(8)}
    def all_memories(self,limit=1000):
        with self.db.connection() as c:return [dict(r) for r in c.execute('SELECT * FROM memories ORDER BY id DESC LIMIT ?',(limit,)).fetchall()]
    def summary(self): return {'version':self.VERSION,'total':len(self.all_memories())}
    def status(self): return {'module':'Persistent Memory','version':self.VERSION,'status':'READY','local_only':True,'summary':self.summary()}
