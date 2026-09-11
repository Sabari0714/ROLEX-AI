from __future__ import annotations
import ast, math, operator, re, sqlite3, time
from pathlib import Path

APP_NAME = 'ROLEX AI'
VERSION = '39.0.0-clean'
DB_PATH = Path.home() / '.rolex_ai_memory.db'

class MathEngine:
    OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
           ast.USub: operator.neg, ast.UAdd: operator.pos}
    def calculate(self, text: str):
        s = text.strip().replace('×','*').replace('÷','/')
        if not re.fullmatch(r'[0-9+\-*/().%\s^]+', s):
            return None
        s = s.replace('^','**')
        try:
            node = ast.parse(s, mode='eval')
            return self._eval(node.body)
        except ZeroDivisionError:
            return 'Division by zero is not allowed.'
        except Exception:
            return None
    def _eval(self, n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int,float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in self.OPS:
            a,b=self._eval(n.left),self._eval(n.right); return self.OPS[type(n.op)](a,b)
        if isinstance(n, ast.UnaryOp) and type(n.op) in self.OPS:
            return self.OPS[type(n.op)](self._eval(n.operand))
        raise ValueError('unsupported expression')

class Memory:
    def __init__(self, path=DB_PATH):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(self.path) as c:
            c.execute('CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, text TEXT, ts REAL)')
    def remember(self, text):
        with sqlite3.connect(self.path) as c: c.execute('INSERT INTO memory(text,ts) VALUES(?,?)',(text,time.time()))
    def recent(self, limit=10):
        with sqlite3.connect(self.path) as c: return [r[0] for r in c.execute('SELECT text FROM memory ORDER BY id DESC LIMIT ?', (limit,))]

class RolexAI:
    def __init__(self): self.math=MathEngine(); self.memory=Memory()
    def ask(self, text):
        raw=text.strip(); low=raw.lower()
        if low.startswith('remember '):
            value=raw[9:].strip(); self.memory.remember(value); return f'நினைவில் வைத்துக்கொண்டேன்: {value}'
        if low in {'memory','show memory','what do you remember'}:
            items=self.memory.recent(); return 'Memory: ' + (' | '.join(items) if items else 'empty')
        result=self.math.calculate(raw)
        if result is not None: return f'Result: {result}'
        if any(x in low for x in ['hello','hi','vanakkam','வணக்கம்']): return 'Vanakkam boss. Rolex AI online.'
        if 'status' in low: return f'{APP_NAME} {VERSION} | local brain: READY | memory: READY | math: READY'
        return f'ROLEX: Command received — {raw}'

# Kivy UI is optional so the same source remains runnable in Termux/Pydroid.
try:
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.graphics import Color, Ellipse, Line, Rectangle
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    KIVY=True
except Exception:
    KIVY=False

if KIVY:
    class HUD(BoxLayout):
        def __init__(self, **kw):
            super().__init__(orientation='vertical', padding=24, spacing=12, **kw)
            self.ai=RolexAI(); self.stage=0
            with self.canvas.before:
                Color(0.015,0.02,0.035,1); self.bg=Rectangle(pos=self.pos,size=self.size)
                Color(0.1,0.5,1,0.8); self.ring=Line(circle=(0,0,90),width=2)
            self.bind(pos=self._draw,size=self._draw)
            self.title=Label(text='ROLEX AI',font_size='34sp',bold=True,size_hint_y=.16)
            self.subtitle=Label(text='INITIALIZING CORE…',font_size='16sp',size_hint_y=.10)
            self.output=Label(text='',font_size='18sp',halign='center',valign='middle',size_hint_y=.34)
            self.input=TextInput(hint_text='Speak / type your command…',multiline=False,size_hint_y=.12)
            self.send=Button(text='SEND',size_hint_y=.10)
            self.send.bind(on_release=lambda *_: self.run())
            self.add_widget(self.title); self.add_widget(self.subtitle); self.add_widget(self.output); self.add_widget(self.input); self.add_widget(self.send)
            Clock.schedule_interval(self.boot, .35)
        def _draw(self,*_):
            self.bg.pos=self.pos; self.bg.size=self.size; self.ring.circle=(self.center_x,self.center_y, min(self.width,self.height)*.23)
        def boot(self,dt):
            self.stage+=1
            labels=['EMBLEM • ZOOM','MECHANICAL DOORS • SPLIT','CORE REVEAL','OPTICAL SYSTEM • BLUE GLOW','HUD ONLINE','ROLEX AI READY']
            if self.stage<=len(labels): self.subtitle.text=labels[self.stage-1]
            else: return False
        def run(self):
            q=self.input.text.strip()
            if q: self.output.text=self.ai.ask(q); self.input.text=''
    class RolexApp(App):
        def build(self): return HUD()

def cli():
    ai=RolexAI(); print(f'{APP_NAME} {VERSION} — CLI READY')
    while True:
        try: q=input('YOU: ').strip()
        except (EOFError,KeyboardInterrupt): break
        if q.lower() in {'exit','quit','shutdown'}: break
        print('ROLEX:',ai.ask(q))

if __name__=='__main__':
    if KIVY:
        RolexApp().run()
    else:
        cli()
