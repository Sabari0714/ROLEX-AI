import ast,operator,re,math
class MathEngine:
    OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow,ast.Mod:operator.mod,ast.USub:operator.neg,ast.UAdd:operator.pos}
    def _eval(self,n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)) and not isinstance(n.value,bool): return n.value
        if isinstance(n,ast.BinOp) and type(n.op) in self.OPS:return self.OPS[type(n.op)](self._eval(n.left),self._eval(n.right))
        if isinstance(n,ast.UnaryOp) and type(n.op) in self.OPS:return self.OPS[type(n.op)](self._eval(n.operand))
        raise ValueError('unsafe expression')
    def safe(self,s):
        s=str(s).strip().replace('×','*').replace('÷','/').replace('^','**')
        if len(s)>500 or not re.fullmatch(r'[0-9+\-*/().%\s]+',s): raise ValueError('unsupported expression')
        return self._eval(ast.parse(s,mode='eval').body)
    def can_handle(self,text):
        t=str(text).lower().strip(); return bool(re.fullmatch(r'[0-9+\-*/().%^\s]+',t)) or t.startswith(('calculate ','calc ','compute ','solve '))
    def calculate(self,text):
        t=str(text).strip(); low=t.lower()
        for p in ('calculate ','calc ','compute ','solve '):
            if low.startswith(p): t=t[len(p):].strip(); break
        m=re.fullmatch(r'(-?[0-9.]+)\s*%\s*(?:of\s*)?(-?[0-9.]+)',t,re.I)
        if m:return {'ok':True,'value':round(float(m.group(1))*float(m.group(2))/100,10),'department':'Mathematics'}
        try:return self.safe(t)
        except ZeroDivisionError:return 'Division by zero is not allowed.'
        except Exception:return None
    def summary(self):return {'engine':'ROLEX_SAFE_MATH','local_only':True}
