class CommandRouter:
    def route(self,text):
        low=str(text).lower().strip()
        if low in {'status','system status'}: return 'status'
        if low.startswith('remember ') or low.startswith('நினைவில்'): return 'memory'
        if low in {'memory','show memory','what do you remember'}: return 'memory'
        if any(x in low for x in ('calculate','calc ','compute ','solve ')): return 'math'
        return 'chat'
