import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

class Database:
    def __init__(self, path):
        p=Path(path).expanduser(); p.parent.mkdir(parents=True,exist_ok=True); self.path=str(p); self._init()
    def connect(self):
        c=sqlite3.connect(self.path); c.row_factory=sqlite3.Row; return c
    @contextmanager
    def connection(self):
        c=self.connect()
        try: yield c; c.commit()
        except Exception: c.rollback(); raise
        finally: c.close()
    def _init(self):
        with self.connection() as c:
            c.executescript('''CREATE TABLE IF NOT EXISTS memories(id INTEGER PRIMARY KEY AUTOINCREMENT,text TEXT NOT NULL,kind TEXT DEFAULT 'fact',importance REAL DEFAULT .5,tags TEXT DEFAULT '[]',created_at TEXT NOT NULL,updated_at TEXT NOT NULL);CREATE TABLE IF NOT EXISTS conversations(id INTEGER PRIMARY KEY AUTOINCREMENT,role TEXT NOT NULL,text TEXT NOT NULL,created_at TEXT NOT NULL);CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,status TEXT DEFAULT 'pending',due_at TEXT,payload TEXT DEFAULT '{}',created_at TEXT NOT NULL,priority TEXT DEFAULT 'normal',project TEXT,notes TEXT,updated_at TEXT);CREATE TABLE IF NOT EXISTS documents(id INTEGER PRIMARY KEY AUTOINCREMENT,path TEXT UNIQUE NOT NULL,name TEXT NOT NULL,content TEXT,updated_at TEXT NOT NULL);CREATE TABLE IF NOT EXISTS cache(key TEXT PRIMARY KEY,value TEXT,expires_at TEXT);CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,event TEXT NOT NULL,details TEXT DEFAULT '{}',created_at TEXT NOT NULL);CREATE TABLE IF NOT EXISTS plans(id INTEGER PRIMARY KEY AUTOINCREMENT,project TEXT NOT NULL,title TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'pending',priority TEXT NOT NULL DEFAULT 'normal',created_at TEXT NOT NULL,updated_at TEXT NOT NULL,completed_at TEXT);CREATE TABLE IF NOT EXISTS plan_steps(id INTEGER PRIMARY KEY AUTOINCREMENT,plan_id INTEGER NOT NULL,step_no INTEGER NOT NULL,title TEXT NOT NULL,task_id INTEGER,status TEXT NOT NULL DEFAULT 'pending',depends_on INTEGER,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,completed_at TEXT);''')
    def add_memory(self,text,kind='fact',importance=.5,tags=None):
        now=datetime.now(timezone.utc).isoformat()
        with self.connection() as c:
            return c.execute('INSERT INTO memories(text,kind,importance,tags,created_at,updated_at) VALUES(?,?,?,?,?,?)',(str(text),kind,float(importance),str(tags or []),now,now)).lastrowid
    def search_memories(self,q,limit=8):
        terms=[x.lower() for x in str(q).split() if len(x)>1]
        with self.connection() as c: rows=c.execute('SELECT * FROM memories ORDER BY importance DESC,updated_at DESC LIMIT 500').fetchall()
        scored=[]
        for r in rows:
            s=sum(t in r['text'].lower() for t in terms)
            if s: scored.append((s,dict(r)))
        return [r for _,r in sorted(scored,key=lambda x:x[0],reverse=True)[:limit]]
    def recent_messages(self,limit=8):
        with self.connection() as c: return [dict(r) for r in c.execute('SELECT * FROM conversations ORDER BY id DESC LIMIT ?',(limit,)).fetchall()]
    def add_message(self,role,text):
        now=datetime.now(timezone.utc).isoformat()
        with self.connection() as c: c.execute('INSERT INTO conversations(role,text,created_at) VALUES(?,?,?)',(role,str(text),now))
