from __future__ import annotations
import threading
try:
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    KIVY_AVAILABLE=True
except Exception:
    KIVY_AVAILABLE=False

if KIVY_AVAILABLE:
    class RolexHUD(BoxLayout):
        def __init__(self,core=None,**kwargs):
            super().__init__(orientation='vertical',padding=20,spacing=12,**kwargs); self.core=core
            self.title=Label(text='ROLEX AI',font_size='30sp',size_hint_y=.15); self.add_widget(self.title)
            self.status=Label(text='LOCAL CORE • READY',size_hint_y=.1); self.add_widget(self.status)
            self.output=Label(text='',halign='left',valign='top'); self.add_widget(self.output)
            self.input=TextInput(hint_text='Speak or type to ROLEX...',multiline=False,size_hint_y=.12); self.add_widget(self.input)
            b=Button(text='SEND',size_hint_y=.12); b.bind(on_release=lambda *_:self.send()); self.add_widget(b)
        def send(self):
            q=self.input.text.strip()
            if not q or self.core is None:return
            self.input.text=''; self.output.text='ROLEX: processing...'
            def work():
                try:r=self.core.ask(q)
                except Exception as e:r=f'Error: {e}'
                Clock.schedule_once(lambda *_:setattr(self.output,'text',str(r)),0)
            threading.Thread(target=work,daemon=True).start()
    class RolexApp(App):
        title='ROLEX AI'
        def __init__(self,core_factory=None,**kwargs):super().__init__(**kwargs);self.core_factory=core_factory
        def build(self):return RolexHUD(core=self.core_factory() if self.core_factory else None)
else:
    class RolexApp:
        def __init__(self,*a,**k):raise RuntimeError('Kivy is required to launch ROLEX UI')
